from classes.game_state import GameState
from classes.choice import Choice
from tools import config

def get_command_help(_game = None, _in_msg = None) -> str:
    return config.file_to_str("command_help.txt")

# Intentionally undocumented. We will tell people about this one
# when they start a new game.
def get_credits(_game = None, _in_msg = None) -> str:
    return config.file_to_str("credits.txt")

COMMANDS = {
    "BEGIN":   GameState.start_new_game,
    "DELETE":  GameState.delete_save,
    "LAST":    GameState.get_last_message,
    "HELP":    get_command_help,
    "CREDITS": get_credits,

    # Aliases
    "FORGET":  GameState.delete_save,
    "REPEAT":  GameState.get_last_message,
}

NO_SAVE_MSG = Choice("0").message

def handle_input(game: GameState, in_msg: str) -> str:
    found_cmd = COMMANDS.get(in_msg)

    if found_cmd:
        out_msg = found_cmd(game, in_msg)
    elif game.load():
        out_msg = game.run(in_msg)
        game.save()
    else:
        out_msg = NO_SAVE_MSG

    return out_msg
