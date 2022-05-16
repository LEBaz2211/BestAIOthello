    ___  _   _        _ _     
   / _ \| |_| |_  ___| | |___ 
  | (_) |  _| ' \/ -_) | / _ \
   \___/ \__|_||_\___|_|_\___/

IT project June 2022
Basil Mannaerts (20269)
Yllke Prebreza (18402)

QUICK LAUNCH:

    Go to the "game_runner.py" file, change the server addresses in player1 object creation, then run the file.

A. The AI implementation

Libraries used : easyAI, numpy

    - EsayAI is a pure-Python artificial intelligence framework for two players games. This 
    library makes it easy to define the mechanism of a game and, in our case, play it against 
    the computer. Under the hood, the AI is a NegaMax algorithm with alpha-beta prunning.

    - Numpy is a python library generally used to create array objects, we thought that by using numpy 
    we would easely have access to the different positions on the board and we could easely go through it 
    to collect information for the AI.

B. Player file

Libraries used : socket, json, threading, time

All these libraries are used to save data and enable communication between our AI and the server 
given by the teacher.

C. Game_runner

It gives a nicer file to use to launch the game. This file mainly uses the player file as a library
to start the game.

D. To run the code :

    1. Enter python server.py othello on your terminal  (on MacOS, you have to specify the python 
    version, to do so you need to use python3 server.py othello)

    2. Run file game_runner.py

