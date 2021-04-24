# coding: utf-8
import re
import time
from os import path
from pathlib import Path

import Constants
from Constants import States
from model.Grid import Grid
from model.History import History


class Game:
    """
    A Game consists in:
        - a current score variable
        - an ended game flag
        - a round count variable
        - a Grid object
        - an History object
    """

    def __init__(self, grid, init_grid_with_two_tiles, display_grid=True):
        """
        Init method to initialize a new Game from an empty Grid object

        @param grid: an empty numpy Grid object
        @type grid: Grid
        @param init_grid_with_two_tiles: whether or not to generate too random tiles to start
        @type init_grid_with_two_tiles: bool
        @param display_grid: whether or not to print the initial state of the 2048 game
        @type display_grid: bool
        """
        self.current_score = 0
        self.ended_game = False
        self.round_count = 0
        self.grid = grid
        self.history = History(grid.nb_rows, grid.nb_columns)
        if init_grid_with_two_tiles:
            self.grid.generate_new_number(self.grid.return_free_positions())
            self.grid.generate_new_number(self.grid.return_free_positions())
            self.history.add_grid_state(self.grid.to_string(), 0)
        if display_grid:
            print(self.__repr__())

    def __repr__(self):
        """
        Utility method to print info about a current Game object

        Returns a string with:
            - Current round number
            - Current score
            - Current Grid state

        @return: Game object representation
        @rtype: str
        """
        str_to_return = "Round: {}\n".format(self.round_count)
        str_to_return += "Score: {}\n\n".format(self.current_score)
        str_to_return += self.grid.__str__()
        return str_to_return

    def play_one_direction(self, direction, index_choice):
        """
        Method to play one direction on the Grid object associated to this Game

        @param direction: one of the defined directions from the Constants file
        @type direction: Constants.Directions
        @param index_choice: the index of the chosen direction (0 was the first choice, 3 was the last choice)
        @type index_choice: int

        @return: whether or not it was a valid move (i.e. at least one tile moved)
        @rtype: bool
        """
        self.grid.move_tiles(direction)
        self.current_score += self.grid.merge(direction)
        self.grid.move_tiles(direction)
        if self.history.something_moved(self.grid.to_string()):
            self.history.add_direction_or_state(direction, index_choice)
            print("Next direction to be played: {}".format(direction.value))
            print("=======================================")  # To distinguish from next round
            self.round_count += 1
            self.grid.generate_new_number(self.grid.return_free_positions())
            self.history.add_grid_state(self.grid.to_string(), self.current_score)
            print(self.__repr__())
            self.check_win_or_loose()
            return True
        else:
            return False

    def play_many_directions(self, direction_list):
        """
        Method to play one direction from a list on the Grid object associated to this Game
        The method plays one direction at maximum and then exits if it was a valid move
        If no direction can be played, the method exits

        @param direction_list: the directions to be played sorted by order of preference (index 0 will be tried first)
        @type direction_list: list of Constants.Directions
        """
        for i in range(len(direction_list)):
            if self.play_one_direction(direction_list[i], i):
                break

    def check_win_or_loose(self):
        """
        Method to update the ended_game flag in case of victory or loss
        """
        if self.grid.is_winning():
            self.ended_game = True
            self.history.add_direction_or_state(States.WIN, -1)
            print("YOU WIN!!!\n")
        elif not self.grid.move_is_still_possible():
            self.ended_game = True
            self.history.add_direction_or_state(States.LOOSE, -1)
            print("Sorry, you loose...\n")
        else:
            # The game continues (i.e. self.ended_game = False)
            pass

    def save_game(self, base_path):
        """
        Utility method to save the History of a Game into file for later inspection

        @param base_path: the complete directory path where to write the log file
        @type base_path: str
        """
        Path(base_path).mkdir(parents=True, exist_ok=True)  # Require Python 3.4+
        file_path = path.join(base_path, "{}.log".format(int(time.time())))
        with open(file_path, 'w') as f:
            f.write("{} {}\n".format(self.grid.nb_rows, self.grid.nb_columns))
            f.write(self.history.__repr__())
            f.flush()

    @staticmethod
    def load_game(log_file_path, display_grid=True):
        """
        Static method to load a 2048 game log to visualize it through the GUI

        @param log_file_path: the path of the log to load
        @type log_file_path: str
        @param display_grid: whether or not to print the initial state of the 2048 game
        @type display_grid: bool

        @return: a Game object that contains all the game history (tile positions, directions and score)
        @rtype: Game
        """
        with open(log_file_path, 'r') as f:
            nb_rows_columns = int(f.readline().strip().split(' ')[0])
            grid = Grid(nb_rows_columns)
            game = Game(grid, init_grid_with_two_tiles=False, display_grid=display_grid)
            line = f.readline()
            while line:
                l_split = line.strip().split(' ')
                if len(l_split) > 3:
                    game.history.score_history.append(int(l_split[1]))
                    game.history.grid_history.append(' '.join(l_split[2:-2]))
                    if l_split[-2] != "WIN" and l_split[-2] != "LOOSE":
                        game.history.direction_state_history.append(Constants.Directions(l_split[-2]))
                    else:
                        game.history.direction_state_history.append(Constants.States(l_split[-2]))
                    m = re.search(r"\[([-0-9]+)\]", l_split[-1])  # Regex to extract index from brackets
                    game.history.direction_index_history.append(int(m.group(1)))
                line = f.readline()
        return game
