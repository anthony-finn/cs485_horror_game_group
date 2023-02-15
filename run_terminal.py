#!/usr/bin/python3
"""
A terminal interface that simulates SMS. It has two purposes: testing the game
locally, and reducing Prof. Jardin's SMS bill while we do so.
"""

from classes.game_state import GameState
from bin.handle_input import handle_input
from sys import stdin, stdout

def main():
    game = GameState('local_terminal')
    print("Terminal SMS simulator ready!")

    # Main game loop
    while True:
        print("> ", end="")
        stdout.flush()
        in_msg = stdin.readline()
        if not in_msg: # If we read EOF
            print() # Send one last \n for the coming shell prompt, as a courtesy.
            break

        out_msg = handle_input(game, in_msg[:-1])

        print(
            out_msg,
            end='' if out_msg[-1] == '\n' else '\n')
        stdout.flush()

if __name__ == "__main__": main() # Execute only if this file is run directly
