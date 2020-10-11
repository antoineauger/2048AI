# coding: utf-8
from enum import Enum  # Require Python 3.4+


class Directions(Enum):
    RIGHT = 'Right'
    LEFT = 'Left'
    UP = 'Up' 
    DOWN = 'Down'


class States(Enum):
    WIN = 'WIN'
    LOOSE = 'LOOSE'


class Modes(Enum):
    MODE_PLAY = 'MODE_PLAY'
    MODE_REPLAY = 'MODE_REPLAY'


GRID_NB_ROWS_COLUMNS = 4
TILE_NUMBER_TO_WIN = 2048
DATA_DIR_NAME = 'data'
