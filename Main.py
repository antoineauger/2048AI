# coding: utf-8
from os import path
from random import shuffle

import numpy as np
import Constants
from Constants import Directions
from ai.Layer import Layer
from ai.NeuralNetwork import NeuralNetwork
from model.Game import Game
from model.Grid import Grid

# We create a new empty Grid object
grid = Grid(nb_rows_columns=Constants.GRID_NB_ROWS_COLUMNS)
# We create a Game from that Grid with two tiles to start
game = Game(grid, init_grid_with_two_tiles=True)

# The list of directions that can be played
directions = [Directions.LEFT, Directions.RIGHT, Directions.UP, Directions.DOWN]

# You can choose between RANDOM, NEURAL and STATS modes
mode = "STATS"


if mode == "RANDOM":  # --------------- RANDOM test ---------------
    while not game.ended_game:  # While the game is not finished
        shuffle(directions)
        game.play_many_directions(directions)  # We played one of the four directions

elif mode == "NEURAL":  # --------------- NEURAL test ---------------
    nn = NeuralNetwork()  # We create our neural network
    nn.add_layer(Layer(16, 4))  # Only one hidden layer
    nn.add_layer(Layer(4, 4))  # Output layer

    train_dir = path.join(Constants.DATA_DIR_NAME, 'train_logs')
    nn.train_from_directory(directory=train_dir, learning_rate=0.3, max_epochs=400)

    while not game.ended_game:
        x = np.array(np.mat(game.grid.to_string()))
        predictions = nn.predict(x)
        game.play_many_directions(predictions)

elif mode == "STATS":  # --------------- STATS only ---------------
    filepath = path.join(Constants.DATA_DIR_NAME, 'train_logs', 'human_2048_1.log')
    game = Game.load_game(filepath, display_grid=False)

# Finally, we save the game in the replay directory if mode was RANDOM or NEURAL
replay_dir = path.join(Constants.DATA_DIR_NAME,
                       'replays',
                       '{}_{}'.format(Constants.GRID_NB_ROWS_COLUMNS, Constants.GRID_NB_ROWS_COLUMNS))
if mode != "STATS":
    game.save_game(base_path=replay_dir)
game.history.print_stats()
