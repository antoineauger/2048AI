![2048AI_logo](/assets/2048_ai_logo_small.png?raw=true "2048 AI logo")

# 2048AI

Personal project to illustrate how some concepts from Artificial Intelligence (AI) can be applied to the 2048 video game.
If you want more details, please refer to the series of blog posts that I wrote on my personal blog:
1. [Part 1: Presentation](https://antoineauger.fr/blog/2020/03/07/programming-an-ai-based-2048-game-part-1-presentation/)
2. [Part 2: Game Logic](https://antoineauger.fr/blog/2020/10/04/programming-an-ai-based-2048-game-part-2-game-logic/)
3. [Part 3: User Interface](https://antoineauger.fr/blog/2021/02/13/programming-an-ai-based-2048-game-part-3-user-interface/)
4. [Part 4: Neural Network and Wrapping Up](https://antoineauger.fr/blog/2022/01/09/programming-an-ai-based-2048-game-part-4-wrapping-up/)

![2048_gui_start_human](/assets/start_human_fast.gif?raw=true "Example of the start of a 2048 game played by human")

## Project structure

```
2048AI/
│
└───ai/
│   │   Layer.py
│   │   NeuralNetwork.py
│
└───data/
│   └───replays/
│   └───train_logs/
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
│   Constants.py
│   Main.py
```

## Prerequisites

* Python 3.4+
* numpy
* tkinter

## Where to start?

The  entry point of the program is the `Main.py` file. To display the program usage help, simply type:
```
$ python3 Main.py -h
```
Result:
```
usage: Main.py [-h] [--game {HUMAN,RANDOM,NEURAL}] [--path PATH] {PLAY,STATS}

Play a new 2048 game or analyze a finished one

positional arguments:
  {PLAY,STATS}          whether to play or analyze a 2048 game

optional arguments:
  -h, --help            show this help message and exit
  --game {HUMAN,RANDOM,NEURAL}
                        the kind of 2048 game to play
  --path PATH           relative path of the game log file to analyze in the
                        data folder (e.g., train_logs/human_2048_1.log)
```

For the sake of simplicity, some variables are defined in the `Constants.py` file.
By editing this file, you can easily change:
* The number of rows and columns for a squared Grid (default: `4`);
* The tile value required to win a game (default: `2048`);
* The root directory where to save game logs (default: `data`).

Then, to play a new game in an interactive mode with GUI, simply type the following command in your terminal:
```
$ python3 Main.py PLAY --game HUMAN
```

![2048_gui](/assets/gui_play_mode.png?raw=true "2048 GUI play mode")

## Where are stored my game logs?

By default, your game logs are saved in `data/replays`.

For instance, all the game logs corresponding to a 4x4 grid size will be saved in `data/replays/4_4`.

## How to use the replay mode?

Replay mode is only available through the GUI. To start the GUI, enter the command:
```
$ python3 Main.py PLAY --game HUMAN
```
You can then import a previously saved 2048-game log file by clicking on `File > Open game...`.

Then, you can navigate through the game with the directional arrows ( &larr; &rarr; &uarr; &darr; ).

![2048_gui2](/assets/gui_replay_mode.png?raw=true "2048 GUI replay mode")

## How to make an artificial intelligence (AI) play a game?

1. Open the file `Main.py` and design your own Neural Network below the line:
```
# TODO: customize your neural network below
```
You can customize the number of layers (with `add_layer`) as well as the number of neurons 
within each layer (`(Layer(X, Y)`).

Finally, you can also customize the directory used for training (`train_logs` by default), the learning rate (`0.3` by default) as well as the number of 
cycles that the training process should last (`400` by default).

For convenience, all these parameters can be edited in the `Constants.py` file:
```
TRAIN_DIR_NAME = 'train_logs'
NEURAL_NET_TRAINING_RATE = 0.3
NEURAL_NET_MAX_EPOCHS = 400
```
If you are new to AI and/or neural networks, I encourage you to read [this excellent blog post](https://blog.zhaytam.com/2018/08/15/implement-neural-network-backpropagation/) that explains how to 
implement a flexible neural network with backpropagation from scratch.

2. Place the game logs that you want to use to train your Neural Network into the `data/train_logs` directory. 
   Make sure that the logs match the dimensions of the Neural Network you want to train.


3. From your terminal, start the program with the following command:
```
$ python3 Main.py PLAY --game NEURAL
```

4. After training, your AI will play until it wins/looses (spoiler: it is most likely to 
   lose :stuck_out_tongue_winking_eye:).
   When it does, some game stats are displayed before the program ends. 
   
If you want to precisely see which moves your AI played (although it will not tell you why it decided 
to play that way/move), the associated replay is available in `data/replays/`.

```
OK - File parsed: data\train_logs\human_1024_1.log
OK - File parsed: data\train_logs\human_2048_1.log
OK - File parsed: data\train_logs\human_512_1.log
Epoch: #0, MSE: 0.000664
Epoch: #10, MSE: 0.000055
Epoch: #20, MSE: 0.000029

[...]

Sorry, you loose...

Final direction/state: States.LOOSE
Final score: 600
Number of rounds: 68
Max. tile: 64
Avg. points per round: 8.955223880597014
Choice frequencies: {0: 67.16417910447761, 1: 19.402985074626866, 2: 13.432835820895523}

Process finished with exit code 0
```

The question of designing an AI able to always win is, of course, out of the 
scope of this project :grin:. 

Nevertheless, you can read my blog post to understand better why your
AI is (almost) always loosing if you play with a high-target tile (such as 2048).

## How to automatically play a random game?

Simply type the following command in your terminal:
```
$ python3 Main.py PLAY --game RANDOM
```

## How to compute key metrics for a 2048 saved game?

Use the `STATS` mode alongside with the filepath of the 2048 log that you want to analyze. For instance:
```
$ python3 Main.py STATS --path train_logs/human_2048_1.log
```
Result:
```
Final direction/state: States.WIN
Final score: 19984
Number of rounds: 753
Max. tile: 2048
Avg. points per round: 26.574468085106382
Choice frequencies: {0: 100.0}
```