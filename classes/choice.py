import json

class Choice:
    def __init__(self, state_id):
        with open('states.json', 'r') as file:
            data = json.load(file)
            file.close()
        
        for (key, value) in data.items():
            self[key] = value