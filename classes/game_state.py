from classes.choice import Choice
import os
import pickle
import math
import random
import re
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
        self.state = "intro"
        self.last_state = ""
        self.visited_states = []
        self.data = {
            'crystals': [],
            'pickaxe': 1,
            'sword': 1,
            'probability': 0
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

        choice_state = Choice(self.state)
        choices = choice_state.choices

        # Determine if the user's input is a valid action.
        if last_msg in choices:
            cached_state = self.state

            if choices[last_msg] == "LAST_STATE":
                self.state = self.last_state
                next_choice_state = Choice(self.state)
                return next_choice_state.message

            self.state = choices[last_msg]
            next_choice_state = Choice(self.state)
            
            # Apply Data Changes
            if hasattr(next_choice_state, 'data'):
                # Special Game States
                if last_msg == "mine":
                    if next_choice_state.data['crystal'][0] not in self.data['crystals']:
                        if self.data['pickaxe'] == 0:
                            return "You are unable to perform this action! You do not have a pickaxe."
                        else:
                            self.data['crystals'].append(next_choice_state.data['crystal'][0])
                    else:
                        return "You have already collected this crystal fragment!"
                
                # Do not add data if this state has already been visisted
                if self.state not in self.visited_states or (hasattr(next_choice_state, 'repeatable') and next_choice_state.repeatable == True):
                    # Add data
                    for index in next_choice_state.data:
                        value = next_choice_state.data[index]
                        if type(value) in [int, float]:
                            self.data[index] += value
            else:
                # Monster Encounter
                # The chance of the monster must be > 0 and they must perform a movement action.
                if last_msg in ["west", "north", "south", "east"] and self.data['probability'] > 0:
                    chance = self.data['probability']
                    passed = 1 if chance >= 1 else math.floor(random.uniform(0, 1/(1-chance)))
                    if (passed == 1):
                        self.last_state = self.state

                        if self.data['sword'] == 0:
                            if random.choice([True, False]) == True:
                                self.state = "monster - no weapon - success"
                            else:
                                self.state = "monster - no weapon - fail"
                        else:
                            self.state = "monster - weapon"

                        return Choice(self.state).message

            self.visited_states.append(self.state)

            # Special States that are not coordinates shouldnt be placed in last_state
            if re.search(r'[1-9]+, [1-9]+', self.state):
                self.last_state = cached_state

            return next_choice_state.message
        elif hasattr(choice_state, 'next_state'):
            # No Input Required, thus set state to "next_state"
            if choice_state.next_state == "LAST_STATE":
                self.state = self.last_state
                next_choice_state = Choice(self.state)
                return next_choice_state.message
            else:
                self.last_state = self.state
                self.state = choice_state.next_state
                next_choice_state = Choice(self.state)
                self.visited_states.append(self.state)
                return next_choice_state.message

        # Invalid Option, so resend message
        return "Invalid action or command. Text LAST to repeat the previous game message."

    def save(self):
        with open(self.get_save_path(), 'wb') as file:
            pickle.dump(self, file)
