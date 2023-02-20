from classes.choice import Choice
import os
import pickle

from tools.config import PROJECT_ROOT

class GameState:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.load() or self.clear()

    def get_save_path(self) -> str:
        return f"{PROJECT_ROOT}/players/{self.phone_number}.pk"

    def is_loaded(self):
        return getattr(self, "state", None) is not None

    def save_exists(self) -> bool:
        return os.path.exists(self.get_save_path())

    def get_last_message(self, _ = None) -> str:
        if self.save_exists():
            self.load()
            return Choice(self.state).message
        else:
            return "No save game for this phone number. Text BEGIN (in caps) to start a new game."

    def clear(self):
        """Clears the in-memory state data. Does not remove save game on disk!"""
        self.state = None
        self.data = None

    def delete_save(self, _ = None):
        path = self.get_save_path()
        if self.save_exists():
            os.remove(path)
            self.clear()
            return "Save game deleted successfully. Text BEGIN to start a new game."
        else:
            return "No save game for this phone number. Text BEGIN (in caps) to start a new game."

    def start_new_game(self, _ = None) -> str:
        self.state = "1"
        self.data = {
            'minerals': []
        }

        self.save()
        return "Successfully created new save game.\n\n" + self.get_last_message()

    def load(self):
        """
        Attempts to load the save game. Returns `self` if save game has been
        successfully loaded; does nothing and returns `self` if it has already
        been loaded; returns `None` if no save game exists.
        """
        if self.is_loaded():
            return self

        path = self.get_save_path()
        if self.save_exists():
            with open(path, 'rb') as file:
                loaded = pickle.load(file)

                self.state = loaded.state # No way to dereference `self` :/
                self.data = loaded.data

                return self
        else:
            return None

    def run(self, last_msg: str) -> str:
        """Executes one cycle of game logic. Retunrs a message to send to the player."""

        last_msg = last_msg.lower()
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
        return "Invalid action or command. Text LAST to repeat the previous game message."

    def save(self):
        with open(self.get_save_path(), 'wb') as file:
            pickle.dump(self, file)
