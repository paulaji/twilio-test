import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

load_dotenv()

app = Flask(__name__)

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')  # Your Twilio phone number

client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('index.html')

# assigning a global callSid
callSid = None
call = None

# connect call
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
            twiml=f'<Response><Dial>+917548826361</Dial></Response>',
            to=to_phone_number,
            from_=twilio_phone_number
        )

        # store the call sid in a variable to be passed in to the disconnect call route
        callSid = call.sid

        return jsonify({'message': 'Call initiated successfully!', 'call_sid': callSid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# disconnect call
@app.route('/disconnect-call', methods=['POST'])
def disconnect_call():
    try:
        # collect the call_sid
        call_sid = request.json.get("call_sid")
        print(call_sid)

        response = VoiceResponse()
        response.hangup()

        # update the call status
        call = client.calls(call_sid).update(
            twiml=str(response)
        )
        print(call)
        return jsonify({'message': 'Call disconnected successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)

