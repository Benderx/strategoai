# strategoai

Python, C - Using machine learning to learn the game of Stratego.

This repo is used for data generation using monte carlo simulations. Because of the nature of monte carlo simulations, the more samples you can collect the better, so the game engine is written completely in Cython, then compiled to C for speed.

Run driver.py to play x amount of games and store the board states in games.csv. This data is then used in another repo: (to be inserted) to train a CNN on move prediction and board evaluation.