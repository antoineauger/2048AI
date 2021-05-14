# coding: utf-8
import argparse
import pathlib
from os import path
from random import shuffle
import numpy as np
import Constants
from Constants import Directions
from ai.Layer import Layer
from ai.NeuralNetwork import NeuralNetwork
from model.Game import Game
from model.Grid import Grid
from ui.Window import Window

# Parser for command line arguments
my_parser = argparse.ArgumentParser(description='Play a new 2048 game or analyze a finished one', allow_abbrev=False)
my_parser.add_argument('mode', action='store', type=str, choices=['PLAY', 'STATS'],
                       help='whether to play or analyze a 2048 game')
my_parser.add_argument('--game', action='store', type=str, choices=['HUMAN', 'RANDOM', 'NEURAL'],
                       help='the kind of 2048 game to play')
my_parser.add_argument('--path', action='store', type=pathlib.Path,
                       help='relative path of the game log file to analyze in the data folder '
                            '(e.g., train_logs/human_2048_1.log)')
args = my_parser.parse_args()

# Additional checks for parser
if args.mode == 'PLAY' and (args.game is None):
    my_parser.error("PLAY mode requires the --game argument to be given.")
elif args.mode == 'STATS' and (args.path is None):
    my_parser.error("STATS mode requires the --path argument to be given.")

# --------------- PLAY mode ---------------
if args.mode == 'PLAY':
    # We create a new empty Grid object
    grid = Grid(nb_rows_columns=Constants.GRID_NB_ROWS_COLUMNS)
    # We create a Game from that Grid with two tiles to start
    game = Game(grid, init_grid_with_two_tiles=True)

    replay_dir = path.join(Constants.DATA_DIR_NAME,
                           'replays',
                           '{}_{}'.format(Constants.GRID_NB_ROWS_COLUMNS, Constants.GRID_NB_ROWS_COLUMNS))

    # --------------- RANDOM game ---------------
    if args.game == "RANDOM":
        # The list of directions that can be played
        directions = [Directions.LEFT, Directions.RIGHT, Directions.UP, Directions.DOWN]
        while not game.ended_game:  # While the game is not finished
            shuffle(directions)
            game.play_many_directions(directions)  # We played one of the four directions
        game.save_game(base_path=replay_dir)

    # --------------- NEURAL game ---------------
    elif args.game == "NEURAL":
        # TODO: customize your neural network below
        nn = NeuralNetwork()
        nn.add_layer(Layer(16, 4))  # Only one hidden layer
        nn.add_layer(Layer(4, 4))  # Output layer
        # End of neural network customization

        train_dir = path.join(Constants.DATA_DIR_NAME, Constants.TRAIN_DIR_NAME)
        nn.train_from_directory(directory=train_dir,
                                learning_rate=Constants.NEURAL_NET_TRAINING_RATE,
                                max_epochs=Constants.NEURAL_NET_MAX_EPOCHS)

        while not game.ended_game:
            x = np.array(np.mat(game.grid.to_string()))
            predictions = nn.predict(x)
            game.play_many_directions(predictions)
        game.save_game(base_path=replay_dir)

    # --------------- HUMAN game ---------------
    else:
        # No need to create grid or game objects when we launch GUI
        app = Window(nb_rows_columns=Constants.GRID_NB_ROWS_COLUMNS, base_path=replay_dir)
        app.start_new_game()

# --------------- STATS mode ---------------
else:
    filepath = path.join(Constants.DATA_DIR_NAME, args.path)
    game = Game.load_game(filepath, display_grid=False)
    game.history.print_stats()
