"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    # The x coordinate of each line is whole space of the Canvas minus both side margin,
    # and then divided by the the number of years, and add the left side margin and the TEXT DX back.
    space = (width - 2 * GRAPH_MARGIN_SIZE) / len(YEARS)
    return space * (year_index - 1) + GRAPH_MARGIN_SIZE + TEXT_DX


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################
    # Create two lines on the side of the canvas
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE
                       , GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE
                       , CANVAS_HEIGHT - GRAPH_MARGIN_SIZE)

    # Create a line for each decade that x equals the coordination we get from the object,
    for i in range(1, len(YEARS) + 1):
        x = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT)
        canvas.create_text(x, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, text=YEARS[i-1], anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################
    color_index = 0
    for names in lookup_names:
        last_x = 0
        last_y = 0
        for i in range(1, len(YEARS) + 1):
            year = 1900 + (i-1) * 10
            x = get_x_coordinate(CANVAS_WIDTH, i)
            showing_text = names
            showing_text += ' '
            # The y coordination is equal to area between the upper and the lower lines divided by 1000
            # times the rank of the name.
            if str(year) in name_data[names]:
                y = int((CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) * int(name_data[names][str(year)]) / 1000) + \
                    GRAPH_MARGIN_SIZE
                showing_text += "".join(name_data[names][str(year)])

            # If the year is not in the name, than the rank of the year will be *
            # and the y coordinate will be on the bottom line.
            else:
                y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                showing_text += '*'
            canvas.create_text(x, y, text=showing_text, anchor=tkinter.SW, fill=COLORS[color_index % 4])

            # If it was not year 1900, draw a line between the coordinate of last decade and this decade.
            if year != 1900:
                canvas.create_line(x, y, last_x, last_y, width=LINE_WIDTH, fill=COLORS[color_index % 4])
            last_x = x
            last_y = y
        # The color code is different for each name that is shown.
        color_index += 1



# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
