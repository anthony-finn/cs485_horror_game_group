class GameState:
    def __init__(self, phone_number):
        """Creates a new game."""
        self.phone_number = phone_number
        # Initial game state ↓
        self.minerals = []

    def run(self, last_msg: str) -> str:
        """Executes one cycle of game logic. Retunrs the message to send to the player."""
        # TODO: Implement game logic
        return "Hello, world!" # Temporary
