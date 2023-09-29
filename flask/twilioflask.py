import os
from dotenv import load_dotenv
from twilio.rest import Client
from flask import Flask, request, render_template, jsonify

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Retrieve Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')  # Your Twilio phone number

# Create a Twilio client
client = Client(account_sid, auth_token)

# Define a route to render the HTML template
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to handle the AJAX call to initiate the call
@app.route('/make-call', methods=['POST'])
def make_call():
    try:
        # Get the phone number to call from the request
        to_phone_number = request.json.get('to_phone_number')
        
        # Customize your message here
        custom_message = "Hello, this is a custom message from your Flask app!"
        
        # Create a call with a custom TwiML message
        call = client.calls.create(
            # twiml=f'<Response><Say>{custom_message}</Say></Response>',
            twiml=f'<Response><Dial>dial a registered number here because twilio free only supports that</Dial></Response>',
            to=to_phone_number,
            from_=twilio_phone_number
        )

        return jsonify({'message': 'Call initiated successfully!', 'call_sid': call.sid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

