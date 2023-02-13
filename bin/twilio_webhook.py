from flask import request, g
from classes.game_state import GameState
import pickle
import os

from tools.config import yml_configs

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
        from_=yml_configs['twilio']['phone_number'],
        to=request.form['From'])

    with open(path, 'wb') as file:
        pickle.dump(game, file)

    return "OK", 200
