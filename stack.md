# Stack is Back

## Questions

3.1. The init method is an optional method that is called upon the creation of a class object (called instantiation) and instantiates the object with specific values or a specific state. The init method can be defined to take in various arguments which become necessary to pass over when creating the object in order to properly instantiate the object.

3.2. See `parser.py`.

3.3. This method is called whenever the HTML parser encounters a starting tag, where the arguments of the function are the tag it encounted (as a lowercase string) and the parameters of the tag as a dictionary between key and value (ie. <a href="cs50.io"> will have attributes {"href":"cs50.io"} and tag=a).

3.4. The handle_endtag method is called when the HTMLParser encounters an ending tag with the argument tag equal to the lowercase value of the tag (ie. </div> would have tag=div).

3.5. See `parser.py`.

## Debrief

a. http://interactivepython.org/runestone/static/pythonds/BasicDS/ImplementingaStackinPython.html

b. 30 minutes
