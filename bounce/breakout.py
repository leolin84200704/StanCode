"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

The program is a game of brick-breaking. Players hits bricks with a ball,
and controls a paddle to prevent the ball from falling.
Once the ball falls under the paddle, the player loses one life.
Breaking every brick gives the player one point.
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from campy.gui.events.mouse import onmouseclicked

#   Constant
FRAME_RATE = 1000 / 120  # 120 frames per second
NUM_LIVES = 3			 # Number of attempts

#   Global variable
ready_to_start = True    # Once the game starts, "ready_to_start" will become False
                         # to prevent clicking mouse from effecting the game
graphics = BreakoutGraphics(lives=NUM_LIVES)
trial = NUM_LIVES


def main():
    onmouseclicked(start_game)


def start_game(mouse):
    """
    :param(mouse): MouseEvent, players click mouse to initiate the game,
                   and control the paddle by moving the mouse.
    """
    global ready_to_start, trial
    if ready_to_start:
        ready_to_start = False
        x_speed = graphics.get_dx()
        y_speed = graphics.get_dy()
        r = graphics.radius * 2
        while True:
            pause(FRAME_RATE)
            graphics.ball.move(graphics.get_dx(), graphics.get_dy())
            hit = graphics.collide_thing()
            # If the ball hits the wall, the ball bounces back
            if hit is "wall":
                graphics.x_bounce()
            # If the ball hits the paddle or the ceiling, the ball bounces back
            elif hit is "ceiling" or hit is "paddle":
                graphics.y_bounce()
            elif hit is "dead":
                graphics.reset_ball()
                trial -= 1
                # Once the player's lives are used up, the player can no longer restart the game
                if trial > 0:
                    ready_to_start = True
                break
            # If the ball hits a brick, the brick is destroyed and  the ball bounces back
            elif hit is not None:
                graphics.y_bounce()
                graphics.window.remove(hit)
                graphics.show_score()
        # Once the player's lives are used up, the program shows "lose sign"
        if trial <= 0:
            graphics.lose()

    else:
        pass


if __name__ == '__main__':
    main()
