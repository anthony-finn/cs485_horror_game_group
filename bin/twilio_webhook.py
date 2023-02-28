from flask import request, g
from classes.game_state import GameState
from tools.config import yml_configs
from bin.handle_input import handle_input

def handle_request():
    phone_number = request.form['From']
    game = GameState(phone_number)

    out_msg = handle_input(game, request.form['Body'])

    g.sms_client.messages.create(
        body=out_msg,
        from_=yml_configs['twilio']['phone_number'],
        to=request.form['From'])

    game.save()

    return "OK", 200
