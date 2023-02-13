from classes.choice import Choice
import os
import pickle

class GameState:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.state = None
        self.data = None

    def get_save_path(self) -> str:
        return f"players/{self.phone_number}.pk"

    def start_new_game(self):
        self.state = "0"
        self.data = {
            'minerals': []
        }

    def load(self):
        """Attempts to load the save game. Returns `True` if it exists."""
        path = self.get_save_path()
        if os.path.exists(path):
            with open(path, 'rb') as file:
                loaded = pickle.load(file)

                self.state = loaded.state # No way to dereference `self` :/
                self.data = loaded.data

                return self
        else:
            return None

    def run(self, last_msg: str) -> str:
        """Executes one cycle of game logic. Retunrs a message to send to the player."""

        choice_state = Choice(self.state)
        choices = choice_state.choices

        # Determine if the user's input is a valid action.
        if last_msg in choices:
            self.state = choices[last_msg]
            next_choice_state = Choice(self.state)
            return next_choice_state.message
        elif hasattr(choice_state, 'next_state'):
            # No Input Required, thus set state to "next_state"
            self.state = choice_state.next_state
            next_choice_state = Choice(self.state)
            return next_choice_state.message

        # Invalid Option, so resend message
        return choice_state.message

    def save(self):
        with open(self.get_save_path(), 'wb') as file:
            pickle.dump(self, file)
