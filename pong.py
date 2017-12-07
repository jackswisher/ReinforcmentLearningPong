import pygame  # to make Graphical User Interface games in python
import random  # to randomize direction ball starts moving in
import time  # to allow function to pause for a small amount of time before getting next frame

# size of our window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# size of our paddle
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60

# size of our ball
BALL_RADIUS = 5

# speeds of our paddle and ball
PADDLE_SPEED = 5
INITIAL_BALL_X_SPEED = 3
INITIAL_BALL_Y_SPEED = 3

# Speed up constant
SPEED_UP = 1.1

# RGB colors for our paddle and ball
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# initialize our screen using width and height vars
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Paddle 1 is our learning agent
# paddle 2 is the CPU or user controlled paddle (depending on initalized param)


def initializer():
    # get a random number for initial direction of ball
    num = random.randint(0, 9)

    # initialize positions of paddle
    paddle1YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
    paddle2YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2

    # initialize ball x and y directions
    ballXDirection = 1
    ballYDirection = 1

    # starting x position of the ball (middle of the page)
    ballXPos = WINDOW_WIDTH / 2 - BALL_RADIUS

    ballXSpeed = INITIAL_BALL_X_SPEED
    ballYSpeed = INITIAL_BALL_Y_SPEED

    # decide where the ball will move based on the random number
    if(0 < num < 3):
        ballXDirection = 1
        ballYDirection = 1
    if (3 <= num < 5):
        ballXDirection = -1
        ballYDirection = 1
    if (5 <= num < 8):
        ballXDirection = 1
        ballYDirection = -1
    if (8 <= num < 10):
        ballXDirection = -1
        ballYDirection = -1

    # generate a new random number
    num1 = random.randint(0, 9)

    # where it will start, y part
    ballYPos = int(num1 * (WINDOW_HEIGHT - BALL_RADIUS) // 9)

    return [paddle1YPos, paddle2YPos, ballXDirection, ballYDirection, ballXPos, ballYPos, ballXSpeed, ballYSpeed]


def drawBall(ballXPos, ballYPos):
    # draw our ball
    pygame.draw.circle(screen, BLACK, (int(ballXPos + BALL_RADIUS),
                                       int(ballYPos + BALL_RADIUS)), BALL_RADIUS)


def drawPaddle1(paddle1YPos):
    # create first paddle on the left
    paddle1 = pygame.Rect(BALL_RADIUS, paddle1YPos, PADDLE_WIDTH, PADDLE_HEIGHT)

    # draw the paddle
    pygame.draw.rect(screen, BLACK, paddle1)


def drawPaddle2(paddle2YPos):
    # create second paddle on the right
    paddle2 = pygame.Rect(WINDOW_WIDTH - BALL_RADIUS - PADDLE_WIDTH,
                          paddle2YPos, PADDLE_WIDTH, PADDLE_HEIGHT)

    # draw the paddle
    pygame.draw.rect(screen, BLACK, paddle2)


def drawScore(score):
    # draws the score in the top left corner
    font = pygame.font.Font(None, 28)
    scorelabel = font.render("Score " + str(score), 1, BLACK)
    screen.blit(scorelabel, (30, 10))


def drawInfos(infos, action):
    # draws the important info in the top left
    font = pygame.font.Font(None, 15)

    # draws the labels: current step, the mode, epsilon, and the Qmax of the neural net
    label = font.render("step " + str(infos[0]) + " [" + str(infos[3]) + "]", 1, BLACK)
    screen.blit(label, (30, 30))
    label = font.render("epsilon " + str(infos[2]), 1, BLACK)
    screen.blit(label, (30, 45))
    label = font.render("q_max " + str(infos[1]), 1, BLACK)
    screen.blit(label, (30, 60))

    # mode
    actionText = "--"
    if (action[1] == 1):
        actionText = "Up"
    if (action[2] == 1):
        actionText = "Down"
    label = font.render("action " + actionText, 1, BLACK)
    screen.blit(label, (30, 75))


# update the ball, using the paddle posistions the balls positions and the balls directions
def updateBall(paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection, ballXSpeed, ballYSpeed):

    # update the x and y position
    ballXPos = int(ballXPos + ballXDirection * ballXSpeed)
    ballYPos = int(ballYPos + ballYDirection * ballYSpeed)

    score = 0

    # checks for a collision between the ball and our learning paddle (paddle1)
    if (ballXPos <= BALL_RADIUS + PADDLE_WIDTH):
        if (ballYPos + 2 * BALL_RADIUS >= paddle1YPos and ballYPos <= paddle1YPos + PADDLE_HEIGHT):
            # switches directions
            ballXDirection = 1
            # speeds up
            ballXSpeed = ballXSpeed * SPEED_UP
            ballYSpeed = ballYSpeed * SPEED_UP
            # score for not letting the ball through
            score = 1
        # otherwise if ball goes through
        elif ballXPos < 0:
            # negative score
            score = -1
            # reset paddle to middle and randomize direction of ball
            [paddle1YPos, paddle2YPos, ballXDirection, ballYDirection,
                ballXPos, ballYPos, ballXSpeed, ballYSpeed] = initializer()

        return [score, paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection, ballXSpeed, ballYSpeed]

    # checks for a collision between the ball and the right paddle
    if (ballXPos + 2 * BALL_RADIUS >= WINDOW_WIDTH - PADDLE_WIDTH - BALL_RADIUS):
        if (ballYPos + 2 * BALL_RADIUS >= paddle2YPos and ballYPos <= paddle2YPos + PADDLE_HEIGHT):
            # switch directions
            ballXDirection = -1
            # speed up
            ballXSpeed = ballXSpeed * SPEED_UP
            ballYSpeed = ballYSpeed * SPEED_UP
        # otherwise if ball goes through
        elif ballXPos + 2 * BALL_RADIUS > WINDOW_WIDTH:
            # positive score
            score = 1
            # reset paddle to middle and randomize direction of ball
            [paddle1YPos, paddle2YPos, ballXDirection, ballYDirection,
                ballXPos, ballYPos, ballXSpeed, ballYSpeed] = initializer()
        return [score, paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection, ballXSpeed, ballYSpeed]

    # if the ball hits the top of the screen, move down
    if (ballYPos <= 0):
        ballYPos = 0
        ballYDirection = 1
    # if the ball hits the bottom of the screen, move up
    elif (ballYPos + 2 * BALL_RADIUS >= WINDOW_HEIGHT):
        ballYPos = WINDOW_HEIGHT - 2 * BALL_RADIUS
        ballYDirection = -1

    return [score, paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection, ballXSpeed, ballYSpeed]


# update the first paddle's position
def updatePaddle1(action, paddle1YPos):
    # if the action is to move up
    if (action[1] == 1):
        paddle1YPos -= PADDLE_SPEED
    # if the action is to move down
    if (action[2] == 1):
        paddle1YPos += PADDLE_SPEED

    # do not allow the paddle to move off the screen
    # if paddle hits top of the page; let it stay there
    if (paddle1YPos < 0):
        paddle1YPos = 0
    # if paddle hits bottom of the page; let it stay there
    if (paddle1YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle1YPos = WINDOW_HEIGHT - PADDLE_HEIGHT

    # return the position of paddle1
    return paddle1YPos


def updatePaddle2(paddle2YPos, ballYPos, user_playing):
    if not user_playing:
        # move the ball down if it is in the upper half
        if paddle2YPos + PADDLE_HEIGHT / 2 < ballYPos + BALL_RADIUS:
            paddle2YPos = paddle2YPos + PADDLE_SPEED
        # move the ball up if it is in the lower half
        if paddle2YPos + PADDLE_HEIGHT / 2 > ballYPos + BALL_RADIUS:
            paddle2YPos = paddle2YPos - PADDLE_SPEED
        # if paddle hits top of the page; let it stay there
        if paddle2YPos < 0:
            paddle2YPos = 0
        # if paddle hits bottom of the page; let it stay there
        if paddle2YPos > WINDOW_HEIGHT - PADDLE_HEIGHT:
            paddle2YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    else:
        # if the down key is pressed, move down
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            paddle2YPos += PADDLE_SPEED
        # if the up key is pressed, move up
        elif pygame.key.get_pressed()[pygame.K_UP]:
            paddle2YPos -= PADDLE_SPEED
        # if paddle hits top of the page; let it stay there
        if paddle2YPos < 0:
            paddle2YPos = 0
        # if paddle hits bottom of the page; let it stay there
        if paddle2YPos > WINDOW_HEIGHT - PADDLE_HEIGHT:
            paddle2YPos = WINDOW_HEIGHT - PADDLE_HEIGHT

    return paddle2YPos


# game class
class PongGame:
    def __init__(self, user_playing):
        pygame.font.init()
        # keep score
        self.tally = 0
        self.user_playing = user_playing

        # initialize each relevant variable
        [self.paddle1YPos, self.paddle2YPos, self.ballXDirection, self.ballYDirection,
            self.ballXPos, self.ballYPos, self.ballXSpeed, self.ballYSpeed] = initializer()

    def getCurrentFrame(self):
        # calls the event queue for each frame
        pygame.event.pump()
        # make the background WHITE
        screen.fill(WHITE)
        # draw each of our paddles
        drawPaddle1(self.paddle1YPos)
        drawPaddle2(self.paddle2YPos)
        # draw our ball
        drawBall(self.ballXPos, self.ballYPos)
        # draw our score
        drawScore(self.tally)
        # copies the pixels from our surface to a 3D array. (basically draws the game)
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        # updates the window
        pygame.display.flip()

        # return our surface data
        return image_data

    # update our screen
    def getNextFrame(self, action, infos):
        score = 0
        # update our paddle
        self.paddle1YPos = updatePaddle1(action, self.paddle1YPos)
        # update evil AI paddle
        self.paddle2YPos = updatePaddle2(self.paddle2YPos, self.ballYPos, self.user_playing)
        # update our vars by updating ball position
        [score, self.paddle1YPos, self.paddle2YPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection, self.ballXSpeed, self.ballYSpeed] = updateBall(
            self.paddle1YPos, self.paddle2YPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection, self.ballXSpeed, self.ballYSpeed)
        # use getCurrentFrame to redraw paddle and ball and copy the pixels
        image_data = self.getCurrentFrame()
        # draw the relevant information on the page for training paddle1
        drawInfos(infos, action)

        # update the window after all changes
        pygame.display.flip()

        # record the total score
        self.tally = self.tally + score
        drawScore(self.tally)

        # if the "X" button is clicked, close the page
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # return the score and the surface data
        return [score, image_data]