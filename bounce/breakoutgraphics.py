"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmousemoved
import random

# Constant
BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).
INITIAL_Y_SPEED = 2    # Initial vertical speed for the ball.
MAX_X_SPEED = 1        # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:
    """
    The class depicts a world the contains: ball, bricks, paddle, score, remaining_lives,
    and the sign of whether the player wins or loses.
    """
    def __init__(self, ball_radius = BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING, lives = 3,
                 title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.pad_off = paddle_offset
        self.paddle = GRect(width=paddle_width, height=paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.window.add(self.paddle, x=(window_width-paddle_width)/2, y=window_height-paddle_height-paddle_offset)
        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.radius = ball_radius
        self.window.add(self.ball, x=window_width/2-ball_radius, y=window_height/2-ball_radius)
        # Default initial velocity for the ball
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = -self.__dx
        # Draw bricks
        for i in range(brick_cols):
            if i == 0 or i == 1:
                color = 'red'
            elif i == 2 or i == 3:
                color = 'orange'
            elif i == 4 or i == 5:
                color = 'yellow'
            elif i == 6 or i == 7:
                color = 'green'
            else:
                color = 'navy'
            for j in range(brick_rows):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                self.brick.color = color
                self.brick.fill_color = color
                self.window.add(self.brick, x=j * (brick_width + brick_spacing), y=i * (brick_height + brick_spacing))
        # Show score
        self.score = 0
        self.label = GLabel('Score: ' + str(self.score), x=50, y=50)
        self.label.font = '-25'
        self.window.add(self.label, x=0, y=630)
        # Show lives
        self.lives = lives
        self.label2 = GLabel('Remain Lives: ' + str(self.lives), x=50, y=50)
        self.label2.font = '-18'
        self.window.add(self.label2, x=200, y=630)
        # Show lose sign
        self.label3 = GLabel('You lose! ', x=50, y=50)
        self.label3.font = '-50'
        # Show win sign
        self.label4 = GLabel('You win! ', x=50, y=50)
        self.label4.font = '-50'
        # Initialize our mouse listeners
        onmousemoved(self.move_paddle)

    def move_paddle(self, mouse):
        if mouse.x > self.paddle.width/2 and (mouse.x < self.window.width - self.paddle.width/2):
            self.paddle.x = mouse.x - self.paddle.width/2

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def x_bounce(self):
        self.__dx *= -1

    def y_bounce(self):
        self.__dy *= -1

    def reset_ball(self):
        """
        Reset the ball the original point, restart the game after the player click the mouse again
        """
        self.window.add(self.ball, x=self.window.width/2, y=self.window.height/2-self.ball.height)
        self.lives -= 1
        self.label2.text = ('Remain Lives: ' + str(self.lives))

    def show_score(self):
        """
        After the player destroy a brick, the player gets one point and the point is shown in the program
        """
        self.score += 1
        self.label.text = ('Score: ' + str(self.score))
        if self.score == 100:
            self.win()

    def lose(self):
        self.window.add(self.label3, x=self.window.width/2-100, y=self.window.height/2-self.ball.height)

    def win(self):
        self.window.add(self.label4, x=self.window.width / 2 - 100, y=self.window.height / 2 - self.ball.height)

    def collide_thing(self):
        for x in range(int(self.ball.x), int(self.ball.x + 2 * BALL_RADIUS + 1), BALL_RADIUS * 2):
            for y in range(int(self.ball.y), int(self.ball.y + 2 * BALL_RADIUS + 1), BALL_RADIUS * 2):
                maybe_thing = self.window.get_object_at(x, y)
                if x >= self.window.width or x <= 0:
                    return "wall"
                if y <= 0:
                    return "ceiling"
                if y >= self.window.height:
                    return "dead"
                if maybe_thing is not None and maybe_thing is not self.label and maybe_thing is not self.label2:
                    if maybe_thing is self.paddle:
                        if self.ball.y + 2 * BALL_RADIUS <= int(self.window.height - PADDLE_OFFSET - PADDLE_HEIGHT + 2):
                            return "paddle"
                        return None
                    return maybe_thing
        return None



