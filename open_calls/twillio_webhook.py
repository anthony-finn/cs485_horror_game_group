import yaml
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json

yml_configs = {}
with open('config.yml', 'r') as yml_file:
    yml_configs = yaml.safe_load(yml_file)



def handle_request():
    print(request.form) #['Body'])

    message = g.sms_client.messages.create(
                     body=request.form['Body'],
                     from_=yml_configs['twillio']['phone_number'],
                     to=request.form['From'])

    return json_response( status = "ok" )
