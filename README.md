# 2048AI

Personal project to illustrate how some concepts from Artificial Intelligence (AI) can be applied to the 2048 video game.
If you want more details, please refer to the series of blog posts that I wrote on my personal blog:
1. [Part 1: Presentation](https://antoineauger.fr/blog/2020/03/07/programming-an-ai-based-2048-game-part-1-presentation/)
2. [Part 2: Game Logic](https://antoineauger.fr/blog/2020/10/04/programming-an-ai-based-2048-game-part-2-game-logic/)
3. Part 3: Stay tuned!

![2048_gui](/assets/gui_play_mode.png?raw=true "2048 GUI play mode")

## Project structure

```
2048AI/
│
└───data/
│
└───model/
│   │   Game.py
│   │   Grid.py
│   │   History.py
│
└───ui/
│   │   TkConstants.py
│   │   Window.py
│
│   Application.py
│   Constants.py
│   Main.py
```

## Prerequisites

* Python 3.4+
* numpy

## How to play?

The  entry point of the program is the `Main.py` file.
Add/comment all the logic you want to execute there. 

For the sake of simplicity, some interesting variables are defined in the `Constants.py` file.
By editing this file, you can easily change:
* The number of rows and columns for a squared Grid (default: 4);
* The tile value required to win a game (default: 2048);
* The root directory where to save game logs (default: `data`).

Then, to launch the game, simply type:
```
$ python3 Main.py
```

If you prefer to play in an interactive manner through the GUI:
```
$ python3 Application.py
```

## Where are stored my game logs?

By default, your game logs are saved in `data/replays`.

For instance, all the game logs corresponding to a 4x4 grid size will be saved in `data/replays/4_4`.

## How to use the replay mode?

Replay mode is only available through the GUI.
You can import a previously saved 2048-game log file by clicking on `File > Open game...`.

Then, you can navigate through the game with the directional arrows ( &larr; &rarr; &uarr; &darr; ).

![2048_gui2](/assets/gui_replay_mode.png?raw=true "2048 GUI replay mode")
