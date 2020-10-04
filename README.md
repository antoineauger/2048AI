# 2048AI

Personnal project to illustrate how some concepts from Artificial Intelligence (AI) can be applied to the 2048 video game.
If you want more details, please refer to the series of blog posts that I wrote on my personnal blog:
1. [Part 1: Presentation](https://antoineauger.fr/blog/2020/03/07/programming-an-ai-based-2048-game-part-1-presentation/)
2. [Part 2: Game Logic](https://antoineauger.fr/blog/2020/10/04/programming-an-ai-based-2048-game-part-2-game-logic/)

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
│   Main.py
│   Constants.py
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

## Where are stored my game logs?

By default, your game logs are saved in `data/replays`.

For instance, all the game logs corresponding to a 4x4 grid size will be saved in `data/replays/4_4`.

## How to use the replay mode?

Replay mode is only available through the GUI.
More details to come in the next blog post...
