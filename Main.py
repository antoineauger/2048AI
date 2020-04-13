# coding: utf-8
from os import path

import Constants
from Constants import Directions
from model.Game import Game
from model.Grid import Grid

# We create a new empty Grid object
grid = Grid(nb_rows_columns=Constants.GRID_NB_ROWS_COLUMNS)

# We create a Game from that Grid with two tiles to start
game = Game(grid, init_grid_with_two_tiles=True)

# A list of directions to be played (static, for testing purposes)
directions = [Directions.LEFT, Directions.RIGHT, Directions.UP, Directions.DOWN]

while not game.ended_game:  # While the game is not finished
    game.play_many_directions(directions)  # We played one of the four directions

# Finally, we print the game history and save it in the data directory
print("Full History:")
print(game.history)

base_path = path.join(Constants.DATA_DIR_NAME,
                      'replays',
                      '{}_{}'.format(Constants.GRID_NB_ROWS_COLUMNS, Constants.GRID_NB_ROWS_COLUMNS))
game.save_game(base_path=base_path)
