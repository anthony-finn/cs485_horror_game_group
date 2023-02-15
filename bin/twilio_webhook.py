from flask import request, g
from classes.game_state import GameState

from tools.config import yml_configs

def handle_request():
    phone_number = request.form['From']
    game = GameState(phone_number)
    game.load() or game.start_new_game()

    out_msgs = game.run(request.form['Body'])

    for out_msg in out_msgs:
        g.sms_client.messages.create(
            body=out_msg,
            from_=yml_configs['twilio']['phone_number'],
            to=request.form['From'])

    game.save()

    return "OK", 200
