# coding: utf-8
from tkinter.font import BOLD


class TkConstants:
    """
    This class contains some Tk constants
    """

    # Each tile is associated with two hexadecimal codes (
    colors = {'0': ("#cdc0b4", "#cdc0b4"), '2': ("#eee4da", "#776e65"), '4': ("#ede0c8", "#776e65"),
              '8': ("#f2b179", "#f9f6f2"), '16': ("#f59563", "#f9f6f2"), '32': ("#f67c5f", "#f9f6f2"),
              '64': ("#f65e3b", "#f9f6f2"), '128': ("#edcf72", "#f9f6f2"), '256': ("#edcc61", "#f9f6f2"),
              '512': ("#edc850", "#f9f6f2"), '1024': ("#edc53f", "#f9f6f2"), '2048': ("#edc22e", "#f9f6f2")}

    tile_font = ("Courier", 25, BOLD)
    text_font = "Courrier, 15"
    text_small_font = "Courrier, 10"

    border_color = "#92877c"
