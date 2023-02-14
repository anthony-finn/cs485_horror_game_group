from classes.game_state import GameState
from classes.choice import Choice

DEFAULT_MSG = Choice("0").message

def handle_input(game: GameState, in_msg: str) -> str:
    # TODO: Atempt to process the input as a command.
    # This is temporary, so that we still have a way of starting the game.
    # Replace this with a command.
    if in_msg == "BEGIN":
        print("Creating new save game!")
        game.start_new_game()
        out_msg = game.get_last_message() # Show the initial game message
        game.save()

    elif game.load():
        out_msg = game.run(in_msg)
        game.save()
    else:
        out_msg = DEFAULT_MSG

    return out_msg
