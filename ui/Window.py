# coding: utf-8
from tkinter import *
from tkinter import filedialog

from Constants import Modes
from Constants import Directions
from model.Game import Game
from model.Grid import Grid
from ui.TkConstants import TkConstants as tkc


class Window:
    """
    This class represents a tkinter-based 2048 Graphical User Interface (GUI)
    """

    def __init__(self, nb_rows_columns, base_path):
        """
        Init method to initialize a new Tk Window object (GUI)

        @param nb_rows_columns: the number of rows and columns
        @type nb_rows_columns: int
        @param base_path: the complete directory path where to write the log file
        @type base_path: str
        """
        self.mode = Modes.MODE_PLAY
        self.game = None
        self.grid = None
        self.nb_rows = nb_rows_columns
        self.nb_columns = nb_rows_columns
        self.base_path = base_path
        self.label_grid_mat = None

        # General parameters for Tk window
        self.window = Tk()
        self.window.title("AI-based 2048")
        self.window.resizable(0, 0)
        self.window.configure(bg=tkc.colors['0'][0])
        self.window.bind('<KeyRelease>', self.update)

        # Menu
        self.menu = Menu(self.window)
        menu_file = Menu(self.menu, tearoff=0)
        menu_file.add_command(label="New game", command=self.start_new_game)
        menu_file.add_command(label="Open game...", command=self.replay_game)
        self.menu.add_cascade(label="File", menu=menu_file)
        self.window.config(menu=self.menu)

        # Labels
        self.score_text = StringVar()
        self.score_label = Label(master=self.window, textvariable=self.score_text,
                                 font=tkc.text_font, bg=tkc.colors['0'][0])
        self.score_label.grid(sticky="W", row=self.nb_rows, columnspan=self.nb_columns - 1)
        self.mode_text = StringVar()
        self.mode_label = Label(self.window, textvariable=self.mode_text,
                                font=tkc.text_small_font, fg="white")
        self.mode_label.grid(row=self.nb_rows, column=self.nb_columns - 1, rowspan=2)
        self.turn_text = StringVar()
        self.turn_label = Label(self.window, textvariable=self.turn_text,
                                font=tkc.text_font, bg=tkc.colors['0'][0])
        self.turn_label.grid(sticky="W", row=self.nb_rows + 1, columnspan=self.nb_columns - 1)
        self.next_move = StringVar()
        self.next_move_label = Label(self.window, textvariable=self.next_move,
                                     font=tkc.text_small_font, bg=tkc.colors['0'][0])
        self.next_move_label.grid(row=self.nb_rows + 2, columnspan=self.nb_columns)

    def start_new_game(self):
        """
        Method to reset the GUI and start a new GUI
        """
        self.mode = Modes.MODE_PLAY
        self.mode_text.set("PLAY")
        self.next_move.set("Press <c> to cancel")
        if self.label_grid_mat:
            del self.label_grid_mat
        self.label_grid_mat = list()
        self.mode_label.configure(bg="blue")
        grid = Grid(self.nb_rows)
        self.game = Game(grid, init_grid_with_two_tiles=True)
        self.grid = grid
        self.score_text.set("Score: 0")
        self.turn_text.set("Round 0")
        self.display_grid()
        self.window.mainloop()

    def replay_game(self):
        """
        Method to visualize a 2048 game from log file
        """
        self.mode = Modes.MODE_REPLAY
        self.mode_text.set("REPLAY")
        self.mode_label.configure(bg="red")
        filepath = filedialog.askopenfilename(initialdir=".", title="Select file",
                                              filetypes=(("2048 replay files", "*.log"), ("all files", "*.*")))
        if filepath != '':
            self.game = Game.load_game(filepath)
            t_str_state = self.game.history.grid_history[0]
            try:
                self.grid.grid = Grid.from_string(t_str_state, self.nb_rows, self.nb_columns)
                self.update_grid()
            except ValueError:
                print("Incorrect matrix dimensions!")
        else:
            self.start_new_game()

    def display_grid(self):
        """
        Method to display the 2048 grid with Tk
        """
        for r in range(self.nb_rows):
            temp_row_list = list()
            for c in range(self.nb_columns):
                frame = Frame(self.window, width=100, height=100, borderwidth=0, bg=tkc.border_color,
                              relief="solid")
                frame.pack_propagate(False)
                label = Label(frame,
                              text="{}".format(self.grid.grid[r, c]),
                              anchor="center",
                              font=tkc.tile_font,
                              bg=tkc.colors[str(self.grid.grid[r, c])][0],
                              fg=tkc.colors[str(self.grid.grid[r, c])][1])
                label.pack(fill="both", expand=True, padx=5, pady=5)
                frame.grid(row=r, column=c)
                temp_row_list.append(label)
            self.label_grid_mat.append(temp_row_list)

    def update_grid(self):
        """
        Method to update a 2048 grid displayed
        """
        for r in range(self.nb_rows):
            for c in range(self.nb_columns):
                self.label_grid_mat[r][c].configure(text="{}".format(self.grid.grid[r, c]),
                                                    font=tkc.tile_font,
                                                    bg=tkc.colors[str(self.grid.grid[r, c])][0],
                                                    fg=tkc.colors[str(self.grid.grid[r, c])][1])
        self.score_text.set("Score: " + str(self.game.current_score))
        if self.mode == Modes.MODE_REPLAY:
            self.turn_text.set(
                "Round {} / {}".format(self.game.round_count, str(len(self.game.history.grid_history) - 1)))
            self.next_move.set("Next move: {}".format(self.game.history.direction_state_history[self.game.round_count]))
        else:
            self.turn_text.set("Round {}".format(self.game.round_count))
        self.window.update_idletasks()

    def update(self, event):
        """
        Method to react to keyboard events

        @param event: The Tk event fired
        @type event: tkinter.Event
        """
        if self.mode == Modes.MODE_PLAY:
            if event.keysym in [v.value for v in Directions]:
                if not self.game.ended_game:
                    self.game.play_one_direction(Directions(event.keysym), 0)
                    self.update_grid()
                if self.game.ended_game:
                    self.game.save_game(self.base_path)
                    print(self.game.history)
                    print("END OF GAME after {} turns with score {}".format(self.game.round_count,
                                                                            self.game.current_score))
            elif event.keysym in ["c"]:
                self.game.ended_game = False
                if len(self.game.history.grid_history) > 1:
                    self.game.history.direction_state_history.pop()
                    self.game.history.direction_index_history.pop()
                    self.game.history.grid_history.pop()
                    self.game.history.score_history.pop()
                    self.game.round_count -= 1
                    t_str_state = self.game.history.grid_history[-1]
                    self.grid.grid = Grid.from_string(t_str_state, self.nb_rows, self.nb_columns)
                    self.game.current_score = self.game.history.score_history[-1]
                    self.update_grid()

        elif self.mode == Modes.MODE_REPLAY:
            if event.keysym == "Right":
                if self.game.round_count + 1 < len(self.game.history.grid_history):
                    self.game.round_count += 1
            elif event.keysym == "Left":
                if self.game.round_count - 1 >= 0:
                    self.game.round_count -= 1
            elif event.keysym == "Up":
                if self.game.round_count + 50 < len(self.game.history.grid_history):
                    self.game.round_count += 50
                else:
                    self.game.round_count = len(self.game.history.grid_history) - 1
            elif event.keysym == "Down":
                if self.game.round_count - 50 >= 0:
                    self.game.round_count -= 50
                else:
                    self.game.round_count = 0
            t_str_state = self.game.history.grid_history[self.game.round_count]
            self.grid.grid = Grid.from_string(t_str_state, self.nb_rows, self.nb_columns)
            self.game.current_score = self.game.history.score_history[self.game.round_count]
            self.update_grid()
