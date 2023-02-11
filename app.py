#!/home/ubuntu/anaconda3/bin/python3
import traceback
from flask import Flask, make_response, g
from waitress import serve
from bin.twilio_webhook import handle_request
from tools.logging import logger
from tools.secrets import get_secrets
from tools.twilio import get_sms_client

# Initialize Application
app = Flask(__name__)

# App Routing
# Home directory routing
@app.route('/')
def home():
    return "This is a test."

@app.route('/open_api/<proc_name>', methods = ['POST'])
def twilio_webhook(proc_name):
    # Log Webhook Call
    logger.debug(proc_name)
    logger.debug(f"Twilio webhook called.")
    print("hello")
    # Create variables for HTTP response
    response = ''
    code = 200

    # Setup Environment
    g.secrets = get_secrets()
    g.sms_client = get_sms_client()

    # Attempt to execute webhook (calls open_calls.twillio_webhook.handle_request)
    try:
        response, code = handle_request()
    except Exception as error:
        # Log Exception and raise HTTP 500 Internal Server Error
        exception_data = str(Exception) + '\n'
        exception_data = exception_data + str(error) + '\n'
        exception_data = exception_data + traceback.format_exc()
        logger.error(exception_data)
        
        response = 'Internal Server Error'
        code = 500

    # Return HTTP response
    return make_response(response, code)

# Run Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
