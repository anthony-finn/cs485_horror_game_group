#!/usr/bin/python3
"""
A terminal interface that simulates SMS. It has two purposes: testing the game
locally and reducing Prof. Jardin's SMS bill while we're doing so.
"""

from classes.game_state import GameState
import pickle
import os
from sys import stdin, stdout

SAVEGAME = 'players/local_terminal.pk'

def main():
    # Load the game state, or create new if needed.
    if os.path.exists(SAVEGAME):
        with open(SAVEGAME, 'rb') as file:
            game = pickle.load(file)
    else:
        game = GameState('local_terminal.pk')

    print("Terminal SMS simulator ready!")

    # Main game loop
    while True:
        print("> ", end="")
        stdout.flush()
        in_msg = stdin.readline()
        if not in_msg: # If we read EOF
            print() # Send one last \n for the coming shell prompt, as a courtesy.
            break

        out_msg = game.run(in_msg)

        with open(SAVEGAME, 'wb') as file:
            pickle.dump(game, file)

        print(out_msg)
        stdout.flush()

if __name__ == "__main__": main() # Execute only if this file is run directly
