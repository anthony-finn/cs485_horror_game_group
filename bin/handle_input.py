from classes.game_state import GameState
from classes.choice import Choice
from tools import config
from typing import Callable

# Utility functions

def developers_only(fun: Callable[[GameState, str], str]) -> Callable[[GameState, str], str]:
    # Auxillary function; this is what actually gets executed when you
    # invoke a devs-only command.
    def devs_only_aux(game, in_msg):
        developers = config.yml_configs["developers"]
        if game.phone_number in developers:
            return fun(game, in_msg)
        else:
            return "You do not have permission to use this command."

    return devs_only_aux

# Commands

def get_command_help(_game = None, _in_msg = None) -> str:
    return config.file_to_str("command_help.txt")

# Intentionally undocumented. We will tell people about this one
# when they start a new game.
def get_credits(_game = None, _in_msg = None) -> str:
    return config.file_to_str("credits.txt")

def teleport(game: GameState, arg: str) -> str:
    if not arg:
        return "Expected a state id."

    try:
        if not game.load(): return "No save game."

        new_state = Choice(arg)
        game.state = arg
        game.save()

        return f"Teleported to {arg}.\n\n{new_state.message}"

    except KeyError:
        return f"State \"{arg}\" does not exist"

    except Exception as ex:
        return f"Error teleporting to state \"{arg}\": {ex}"

COMMANDS = {
    "BEGIN":   GameState.start_new_game,
    "DELETE":  GameState.delete_save,
    "LAST":    GameState.get_last_message,
    "CMDS":    get_command_help,
    "CREDITS": get_credits,

    "TELEP":   developers_only(teleport),

    # Aliases
    "FORGET":  GameState.delete_save,
    "REPEAT":  GameState.get_last_message,
}

NO_SAVE_MSG = Choice("init").message

# Module entry point

def handle_input(game: GameState, in_msg: str) -> str:
    global COMMANDS

    # Try to find a matching command.
    # Succeeds if `in_msg` starts with the name of a command.
    (cmd_name, found_cmd) = next(
        ((k, v) for (k, v) in COMMANDS.items() if in_msg.startswith(k)),
        (None, None))

    in_msg = in_msg.lower()
    if found_cmd:
        in_msg = in_msg[len(cmd_name) + 1:] # Crop to arguments only
        out_msg = found_cmd(game, in_msg)
    elif game.load():
        out_msg = game.run(in_msg)
        game.save()
    else:
        out_msg = NO_SAVE_MSG

    if out_msg: return out_msg
    else: return "Empty game message; this should not happen."
