import json
from tools.config import PROJECT_ROOT

class Choice:
    def __init__(self, state_id: str):
        with open(PROJECT_ROOT + 'data/states.json', 'r') as file:
            data = json.load(file)
            file.close()

        for key, value in data[state_id].items():
            setattr(self, key, value)