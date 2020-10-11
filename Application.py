# coding: utf-8
from os import path

import Constants
from ui.Window import Window

replay_dir = path.join(Constants.DATA_DIR_NAME,
                       'replays',
                       '{}_{}'.format(Constants.GRID_NB_ROWS_COLUMNS, Constants.GRID_NB_ROWS_COLUMNS))

# No need to create grid or game objects when we launch GUI
app = Window(nb_rows_columns=Constants.GRID_NB_ROWS_COLUMNS, base_path=replay_dir)
app.start_new_game()
