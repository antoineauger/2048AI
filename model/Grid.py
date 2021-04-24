# coding: utf-8
from random import choice

import numpy as np

import Constants
from Constants import Directions


class Grid:
    """
    This class represents a 2048 grid alongside useful methods to print or modify current game state
    """

    def __init__(self, nb_rows_columns, t_str_grid=None):
        """
        Init method to initialize a new squared Grid (nb rows = nb columns) object

        @param nb_rows_columns: the number of rows and columns
        @type nb_rows_columns: int
        @param t_str_grid: (optional) an inline string representation of an existing Grid
        @type t_str_grid: str
        """
        self.nb_rows = nb_rows_columns
        self.nb_columns = nb_rows_columns
        if t_str_grid is None:
            self.grid = np.zeros((self.nb_rows, self.nb_columns), dtype='int64')
        else:
            t_list = [int(i) for i in t_str_grid.strip().split(' ')]
            self.grid = np.reshape(t_list, (self.nb_rows, self.nb_columns))

    def __str__(self):
        """
        Utility method to print the current state of this Grid

        @return: a matrix-like str with line breaks for debugging
        @rtype: str
        """
        str_to_return = ""
        for r in range(self.nb_rows):
            for c in range(self.nb_columns):
                str_to_return += "{}\t".format(self.grid[r, c])
            str_to_return += "\n"
        return str_to_return

    def to_string(self):
        """
        Utility method to get the current inline string representation of this Grid

        @return: the current inline string representation of this Grid
        @rtype: str
        """
        str_to_return = ""
        for r in range(self.nb_rows):
            for c in range(self.nb_columns):
                str_to_return += "{} ".format(self.grid[r, c])
        return str_to_return.strip()

    @staticmethod
    def from_string(t_str_grid, nb_rows, nb_columns):
        """
        Utility method to convert an inline string representation of a Grid into a numpy array (or matrix)

        @param t_str_grid: an inline string representation of a Grid
        @type t_str_grid: str
        @param nb_rows: the number of rows of the final numpy array
        @type nb_rows: int
        @param nb_columns: the number of columns of the final numpy array
        @type nb_columns: int
        @return: a numpy array object corresponding to the inline grid representation
        @rtype: ndarray
        """
        t_list = [int(i) for i in t_str_grid.strip().split(' ')]
        return np.reshape(t_list, (nb_rows, nb_columns))

    def return_free_positions(self):
        """
        Method to get all free positions of a Grid object
        A position is a (x,y) tuple where x refers to the position among rows while y refers to position among columns

        @return: a list of free positions
        @rtype: list of tuples
        """
        free_pos = np.nonzero(self.grid == 0)
        return list(zip(*free_pos))

    def generate_new_number(self, remaining_pos):
        """
        Method to generate a new tile (either a 2 or a 4 tile) and add it to the current grid
        The new tile is chosen from the remaining positions given in parameter

        @param remaining_pos: a list of tuples representing free positions
        @type remaining_pos: list of tuples
        """
        r, c = choice(remaining_pos)
        self.grid[r, c] = choice([2, 4])

    def move_is_still_possible(self):
        """
        Method to determine if a move is still possible given the current Grid state

        A move is still possible if:
            - There is at least one free position
            - There is no free position but two adjacent tiles have the same value

        @return: whether or not a move is still possible
        @rtype: bool
        """
        if self.grid_still_has_room():
            return True
        for r in range(self.nb_rows):
            for c in range(self.nb_columns - 1):
                if self.grid[r, c] == self.grid[r, c + 1]:
                    return True
        for c in range(self.nb_columns):
            for r in range(self.nb_rows - 1):
                if self.grid[r, c] == self.grid[r + 1, c]:
                    return True
        return False

    def grid_still_has_room(self):
        """
        Method to determine if at least one position of this Grid is empty (tile with 0 value)

        @return: whether or not at least one tile has the value 0 (empty)
        @rtype: bool
        """
        return np.count_nonzero(self.grid == 0) > 0

    def is_winning(self):
        """
        Method to determine if the current Grid state is a winning state
        A Grid is in winning state if at least one of its tiles is equals to the TILE_NUMBER_TO_WIN value defined
        in the Constants file

        @return: whether or not the player has won
        @rtype: bool
        """
        return np.count_nonzero(self.grid == Constants.TILE_NUMBER_TO_WIN) > 0

    def move_tiles(self, direction):
        """
        Method to pack all tiles of a Grid according to the given direction
        This method does not merge tiles between them

        @param direction: one of the defined directions from the Constants file
        @type direction: Constants.Directions
        """
        if direction == Directions.RIGHT:
            for r in range(self.nb_rows):
                temp_list = self.grid[r, :][self.grid[r, :] != 0]
                self.grid[r, :] = np.concatenate((np.zeros(self.nb_columns - len(temp_list), ), temp_list))
        elif direction == Directions.LEFT:
            for r in range(self.nb_rows):
                temp_list = self.grid[r, :][self.grid[r, :] != 0]
                self.grid[r, :] = np.concatenate((temp_list, np.zeros(self.nb_columns - len(temp_list), )))
        elif direction == Directions.UP:
            for c in range(self.nb_columns):
                temp_list = self.grid[:, c][self.grid[:, c] != 0]
                self.grid[:, c] = np.array(np.concatenate((temp_list, np.zeros(self.nb_rows - len(temp_list), ))))
        elif direction == Directions.DOWN:
            for c in range(self.nb_columns):
                temp_list = self.grid[:, c][self.grid[:, c] != 0]
                self.grid[:, c] = np.array(np.concatenate((np.zeros(self.nb_rows - len(temp_list), ), temp_list)))

    def merge(self, direction):
        """
        Method to merge adjacent tiles of a Grid according to the given direction
        This method may leave unrealistic free positions and should be followed by a new call to the move_tiles method

        @param direction: one of the defined directions from the Constants file
        @type direction: Constants.Directions
        @return: the score to add to the current score
        @rtype: int
        """
        score_to_add = 0
        if direction == Directions.RIGHT:
            for r in range(self.nb_rows):
                for c in range(self.nb_columns - 1, 0, -1):
                    if self.grid[r, c] == self.grid[r, c - 1]:
                        self.grid[r, c] *= 2
                        score_to_add += self.grid[r, c]
                        self.grid[r, c - 1] = 0
        elif direction == Directions.LEFT:
            for r in range(self.nb_rows):
                for c in range(self.nb_columns - 1):
                    if self.grid[r, c] == self.grid[r, c + 1]:
                        self.grid[r, c] *= 2
                        score_to_add += self.grid[r, c]
                        self.grid[r, c + 1] = 0
        elif direction == Directions.UP:
            for c in range(self.nb_columns):
                for r in range(self.nb_rows - 1):
                    if self.grid[r, c] == self.grid[r + 1, c]:
                        self.grid[r, c] *= 2
                        score_to_add += self.grid[r, c]
                        self.grid[r + 1, c] = 0
        elif direction == Directions.DOWN:
            for c in range(self.nb_columns):
                for r in range(self.nb_rows - 1, 0, -1):
                    if self.grid[r, c] == self.grid[r - 1, c]:
                        self.grid[r, c] *= 2
                        score_to_add += self.grid[r, c]
                        self.grid[r - 1, c] = 0
        return score_to_add
