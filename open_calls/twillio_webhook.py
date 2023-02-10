import yaml
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from player.player import player
import pickle
import os
yml_configs = {}
with open('config.yml', 'r') as yml_file:
    yml_configs = yaml.safe_load(yml_file)



def handle_request():
    phone_number = request.form['From']
    playerObj = None
    if (os.path.exists('players/' + phone_number = '.pk')):
        file = open('players/' + phone_number + '.pk', 'r')
        playerObj = pickle.load(file)
    else:
        playerObj = player(phone_number)

    message = g.sms_client.messages.create(
                     body=request.form['Body'],
                     from_=yml_configs['twillio']['phone_number'],
                     to=request.form['From'])
    
    pickle.dump(
    return json_response( status = "ok" )
