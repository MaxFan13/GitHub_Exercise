import time
import numpy as np
from gridgame import *

##############################################################################################################################

# You can visualize what your code is doing by setting the GUI argument in the following line to true.
# The render_delay_sec argument allows you to slow down the animation, to be able to see each step more clearly.

# For your final submission, please set the GUI option to False.

# The gs argument controls the grid size. You should experiment with various sizes to ensure your code generalizes.
# Please do not modify or remove lines 18 and 19.

##############################################################################################################################

game = ShapePlacementGrid(GUI=True, render_delay_sec=0.5, gs=6, num_colored_boxes=5)
shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute('export')
np.savetxt('initial_grid.txt', grid, fmt="%d")

##############################################################################################################################

# Initialization

# shapePos is the current position of the brush.

# currentShapeIndex is the index of the current brush type being placed (order specified in gridgame.py, and assignment instructions).

# currentColorIndex is the index of the current color being placed (order specified in gridgame.py, and assignment instructions).

# grid represents the current state of the board.

# -1 indicates an empty cell
# 0 indicates a cell colored in the first color (indigo by default)
# 1 indicates a cell colored in the second color (taupe by default)
# 2 indicates a cell colored in the third color (veridian by default)
# 3 indicates a cell colored in the fourth color (peach by default)

# placedShapes is a list of shapes that have currently been placed on the board.

# Each shape is represented as a list containing three elements: a) the brush type (number between 0-8),
# b) the location of the shape (coordinates of top-left cell of the shape) and c) color of the shape (number between 0-3)

# For instance [0, (0,0), 2] represents a shape spanning a single cell in the color 2=veridian, placed at the top left cell in the grid.

# done is a Boolean that represents whether coloring constraints are satisfied. Updated by the gridgames.py file.

##############################################################################################################################


####################################################
# Timing your code's execution for the leaderboard.
####################################################

start = time.time()  # <- do not modify this.


##########################################
# Write all your code in the area below.
##########################################\

def initial_solution(game):
    attempts = 0
    max_attempts = 500  # stop if stuck
    while attempts < max_attempts:
        x = np.random.randint(game.gridSize)
        y = np.random.randint(game.gridSize)
        shapeIndex = np.random.randint(len(game.shapes))
        colorIndex = game.getAvailableColor(game.grid, x, y)

        game.currentShapeIndex = shapeIndex
        game.currentColorIndex = colorIndex
        game.shapePos = [x, y]

        if game.canPlace(game.grid, game.shapes[shapeIndex], [x, y]):
            game.execute("place")
        attempts += 1


def get_score(board, shapes):
    """
    :param board:
    :param shapes:
    :return:
    """
    num_placed = 0
    for row in board:
        for x in row:
            if x != -1:
                num_placed += 1
    num_unique_shapes = len(shapes)
    unique_colors = []
    for shape in shapes:
        color = shape[2]
        if color not in unique_colors:
            unique_colors.append(color)
    num_unique_colors = len(unique_colors)

    score = num_placed - num_unique_shapes * 2 - num_unique_colors * 3
    return score


def generate_neighbor(game):
    if game.placedShapes:
        game.execute("undo")
    x = np.random.randint(game.gridSize)
    y = np.random.randint(game.gridSize)
    shapeIndex = np.random.randint(len(game.shapes))
    colorIndex = game.getAvailableColor(game.grid, x, y)

    game.currentShapeIndex = shapeIndex
    game.currentColorIndex = colorIndex
    game.shapePos = [x, y]

    if game.canPlace(game.grid, game.shapes[shapeIndex], [x, y]):
        game.execute("place")


initial_solution(game)
best_score = get_score(grid, placedShapes)

# Try improving
for i in range(1000):  # number of hill climbing steps
    prev_grid = np.copy(grid)
    prev_shapes = placedShapes[:]

    generate_neighbor(game)
    shapePos, currentShapeIndex, currentColorIndex, grid, placedShapes, done = game.execute("export")
    new_score = get_score(grid, placedShapes)

    if new_score < best_score:
        # Revert if not better
        grid = prev_grid
        placedShapes = prev_shapes
    else:
        best_score = new_score

    if done:
        break


########################################

# Do not modify any of the code below.

########################################

end = time.time()

np.savetxt('grid.txt', grid, fmt="%d")
with open("shapes.txt", "w") as outfile:
    outfile.write(str(placedShapes))
with open("time.txt", "w") as outfile:
    outfile.write(str(end - start))
