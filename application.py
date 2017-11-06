from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    currentuser = session["user_id"]

    # Get the users cash
    cash = db.execute("SELECT cash FROM users WHERE id = :currentuser",
                      currentuser=currentuser)[0].get("cash")

    # Get and store the symbol and quantity of all stocks owned with the quantity > 0
    quantityrow = db.execute("SELECT symbol, SUM(quantity) quantity FROM transactions WHERE user = :currentuser GROUP BY symbol HAVING quantity > 0",
                             currentuser=currentuser)

    # Create a list of dictionaries with the symbol and current price
    stocks = []
    totalvalue = cash

    for row in quantityrow:
        # Retrieve the number of stocks
        quantity = row.get("quantity")

        # Get the symbol and corresponding stock
        symbol = row.get("symbol")
        stock = lookup(symbol)

        # Ensure that the stock exists
        if stock is None:
            return apology("could not lookup stock", 400)

        # Get price and add the price to the dictionary
        price = stock.get("price")
        name = stock.get("name")
        total = quantity * price
        totalvalue += total

        # Create a dictionary with all the requisite data
        data = {
            "symbol": symbol,
            "name": name,
            "quantity": quantity,
            "price": price,
            "total": total
        }

        # Add the completed dictionary to the list
        stocks.append(data)

    # Render the homepage
    return render_template("index.html", stocks=stocks, cash=cash, totalvalue=totalvalue)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST
    if request.method == "POST":

        # Ensure a symbol was entered
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # Ensure a quanity was entered
        elif not request.form.get("shares"):
            return apology("missing shares", 400)

        # Ensure shares is an int
        try:
            quantity = int(request.form.get("shares"))
        except ValueError:
            return apology("invalid shares", 400)

        # Ensure a valid number of shares
        if quantity < 0:
            return apology("invalid shares", 400)

        stock = lookup(request.form.get("symbol"))

        # Ensure stock exists
        if stock is None:
            return apology("invalid symbol", 400)

        # If quantity is not 0, proceed
        if quantity != 0:

            # Retrieve stock data
            name = stock.get("name")
            price = stock.get("price")
            symbol = stock.get("symbol")

            # Retrieve user data
            currentuser = session["user_id"]

            row = db.execute("SELECT cash FROM users WHERE id = :currentuser",
                             currentuser=currentuser)

            # Ensure row exists
            if len(row) != 1:
                return apology("could not find your data", 403)

            # Get available funds
            cash = row[0].get("cash")

            totalcost = price * quantity

            # Ensure user has enough money
            if totalcost > cash:
                return apology("insufficient funds", 400)

            # Update users cash
            remaining = cash - totalcost
            db.execute("UPDATE users SET cash = :remaining WHERE rowid = :currentuser",
                       remaining=remaining, currentuser=currentuser)

            # Store transaction
            db.execute("INSERT INTO transactions(id, user, symbol, price, quantity) VALUES(NULL, :currentuser, :symbol, :price, :quantity)",
                       currentuser=currentuser, symbol=symbol, price=price, quantity=quantity)

        # Redirect to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Render the history page
    transactions = db.execute("SELECT * FROM transactions WHERE user = :currentuser",
                              currentuser=session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add cash to the users account"""

    currentuser = session["user_id"]

    # Get the users cash
    cashrow = db.execute("SELECT cash FROM users WHERE id = :currentuser",
                         currentuser=currentuser)

    # Ensure that the user exists
    if len(cashrow) != 1:
        return apology("could not find user", 400)

    cash = cashrow[0].get("cash")

    # User reached route via POST
    if request.method == "POST":

        # Ensure that user inputted a number
        if not request.form.get("cash"):
            return apology("missing cash to add", 400)

        # Ensure that cashtoadd is a valid number
        cashtoadd = request.form.get("cash")

        # Ensure that cashtoadd is valid
        try:
            # Add cashtoadd to cash and update the user's cash
            cashtoadd = float(cashtoadd)
        except ValueError:
            # Invalid input
            return apology("invalid cash to add", 400)

        if cashtoadd < 0:
            return apology("invalid cash to add", 400)

        # Add cashtoadd to cash and update the user's cash
        cash += cashtoadd

        db.execute("UPDATE users SET cash = :cash WHERE id = :currentuser",
                   cash=cash, currentuser=currentuser)

        # Redirect to home
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("addcash.html", cash=cash)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST
    if request.method == "POST":

        # Ensure the user inputted a symbol
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Get symbol and proceed with lookup
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        # Ensure stock exists
        if stock is None:
            return apology("invalid symbol", 400)

        # Retrieve values
        name = stock.get("name")
        price = stock.get("price")
        symbol = stock.get("symbol")

        # Render page with the stock's data
        return render_template("quoted.html", name=name, price=price, symbol=symbol)

    # User reached route via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""

    # User reached route via POST (ie. submitted a form)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Retrieve values from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Username already exists
        if len(rows) == 1:
            return apology("that username already exists", 400)

        # Password doesn't match the confirmation
        elif password != confirmation:
            return apology("password and confirmation did not match", 400)

        # Calculate the password hash
        pwhash = generate_password_hash(password)

        # Insert new user
        db.execute("INSERT INTO users(id, username, hash) VALUES(NULL, :username, :pwhash)",
                   username=username, pwhash=pwhash)

        # User has been created, redirect to login
        return redirect("/login")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST
    if request.method == "POST":

        # Ensure that user chose a symbol
        if not request.form.get("symbol"):
            return apology("no symbol selected", 400)

        # Ensure that user entered a quantity
        elif not request.form.get("shares"):
            return apology("shares not entered", 400)

        symbol = request.form.get("symbol")

        # Ensure shares is an int
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("invalid shares", 400)

        currentuser = session["user_id"]

        # Ensure shares is a valid number
        if shares < 0:
            return apology("invalid shares", 400)

        # Ensure that the user has enough shares to sell
        quantityrow = db.execute("SELECT SUM(quantity) quantity FROM transactions WHERE user = :currentuser AND symbol = :symbol GROUP BY symbol",
                                 currentuser=currentuser, symbol=symbol)

        # Ensure that the stock is owned
        if len(quantityrow) != 1:
            return apology("stock not owned", 400)

        # Retrieve quantity owned of that share
        quantity = quantityrow[0].get("quantity")

        if quantity < shares:
            return apology("too many shares", 400)

        # Get current price of stock
        stock = lookup(symbol)

        # Ensure symbol is valid
        if stock is None:
            return apology("invalid symbol", 400)

        price = stock.get("price")

        # Create a new transaction to sell the shares
        db.execute("INSERT INTO transactions(id, user, symbol, price, quantity) VALUES(NULL, :currentuser, :symbol, :price, :quantity)",
                   currentuser=currentuser, symbol=symbol, price=price, quantity=-shares)

        # Add the value to cash
        total = price * shares

        row = db.execute("SELECT cash FROM users WHERE id = :currentuser",
                         currentuser=currentuser)

        # Ensure user exists
        if len(row) != 1:
            return apology("user not found", 400)

        cash = row[0].get("cash")
        total += cash

        # Update the user's cash
        db.execute("UPDATE users SET cash = :total WHERE rowid = :currentuser",
                   total=total, currentuser=currentuser)

        # Redirect home
        return redirect("/")

    # User reached route via GET
    else:
        # Get all the symbols for the user with quantity greater than 0
        currentuser = session["user_id"]
        symbols = db.execute("SELECT symbol, sum(quantity) quantity FROM transactions WHERE user = :currentuser GROUP BY symbol HAVING quantity > 0",
                             currentuser=currentuser)

        # Add all valid symbols to a list
        validsymbols = []
        for current in symbols:
            validsymbols.append(current.get("symbol"))

        return render_template("sell.html", symbols=validsymbols)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
