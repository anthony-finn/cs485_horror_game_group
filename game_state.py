class GameState:
    def __init__(self, phone_number):
        """Creates a new game."""
        self.phone_number = phone_number
        # Initial game state ↓
        self.minerals = []

    def run(self, last_msg: str) -> str:
        """Executes one cycle of game logic. Retunrs the message to send to the player."""

        # TODO: Pass `last_msg` to the current state.
        #       There, Determine if the user's input is a valid action.

        # TODO: Transition to a new state as needed.
        #       If there is a new state, get its message (including possible actions)
        #       and return it from this method.

        return "Hello, world!" # Temporary; should return actual game message instead
