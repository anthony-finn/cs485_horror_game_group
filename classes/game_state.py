from classes.choice import Choice

class GameState:
    def __init__(self, phone_number):
        """Creates a new game."""
        self.phone_number = phone_number

        # Initial game state ↓
        self.state = 0
        self.data = {
            'minerals': []
        }

    def run(self, last_msg: str) -> str:
        """Executes one cycle of game logic. Retunrs the message to send to the player."""

        # TODO: Pass `last_msg` to the current state.
        #       There, Determine if the user's input is a valid action.
        choice_state = Choice(self.state)
        # TODO: Transition to a new state as needed.
        #       If there is a new state, get its message (including possible actions)
        #       and return it from this method.
        choices = choice_state.choices
        if last_msg in choices:
            self.state = choices[last_msg]
            next_choice_state = Choice(self.state)
            return next_choice_state.message
        elif "next_state" in choice_state:
            # No Input Required, thus set state to "next_state"
            self.state = choice_state.next_state
            next_choice_state = Choice(self.state)
            return next_choice_state.message

        # Invalid Option, so resend message
        return choice_state.message
