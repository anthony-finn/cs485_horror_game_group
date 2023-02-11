import yaml
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from classes.game_state import GameState
import pickle
import os

with open('config.yml', 'r') as yml_file:
    yml_configs = yaml.safe_load(yml_file)

def handle_request():
    phone_number = request.form['From']
    path = 'players/' + phone_number + '.pk'

    # Load the game state, or create new if needed
    if os.path.exists(path):
        with open(path, 'rb') as file:
            game = pickle.load(file)
    else:
        game = GameState(phone_number)

    out_msg = game.run(request.form['Body'])

    g.sms_client.messages.create(
        body=out_msg,
        from_=yml_configs['twillio']['phone_number'],
        to=request.form['From'])

    with open(path, 'wb') as file:
        pickle.dump(game, file)

    return "OK", 200
