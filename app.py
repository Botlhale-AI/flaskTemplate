from flask import Flask, render_template, request, session, jsonify, make_response
import requests
import json

app = Flask(__name__)
app.secret_key = 'any random string'

# API Endpoints
generateAuthTokenUrl = "https://dev-botlhale.io/generateAuthToken"
connectUrl = "https://dev-botlhale.io/connect"
sendMessageUrl = "https://dev-botlhale.io/message"

# Chatbot Params
with open('config.json') as json_file:
    parameters = json.load(json_file) 

BotID = parameters['BotID']
refreshToken = parameters['refreshToken']
LanguageCode = parameters['LanguageCode']
MessageType = parameters['MessageType']
ResponseType = parameters['ResponseType']

# Front-End Variables
botName="Naledi"
firstBotMessage = """
<p class='chatbot__message'>
    <strong class='intro'>
    Hello, I’m Naledi, your virtual assistant. 
    I'm here to help with your general enquiries.
    </strong>

    Example of questions you can ask for demo purpose: 

    <br>

    <em>
    Hi / How are you? etc.
    </em>
</p>"""


@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html', botName=botName, firstMessage=firstBotMessage)

@app.route('/startConversation')
def startConversation():
    # Generate IdToken for Bearer Auth on other endpoints.
    payload={
        'REFRESH_TOKEN': refreshToken,
        }
    IdToken = json.loads(requests.request("POST", generateAuthTokenUrl, data=payload).content)['AuthenticationResult']['IdToken']

    # Generate ConversationID.
    payload={
        'BotID': BotID,
        'LanguageCode': LanguageCode
        }
    headers = {"Authorization": "Bearer {}".format(IdToken)}
    ConversationID = json.loads(requests.request("POST", connectUrl, headers=headers, data=payload).content)['ConversationID']

    # Store ConversationID & IdToken in the session for use in the sendMessage route.
    session['ConversationID'] = ConversationID
    session['IdToken'] = IdToken

    return make_response(jsonify({"ConversationID":ConversationID, "IdToken":IdToken}), 200)

@app.route('/sendMessage', methods = ['GET'])
def sendMessage():
    # Get session variables
    ConversationID = session['ConversationID']
    IdToken = session['IdToken']

    # Get request parameters
    TextMsg = request.args.get('text')

    # Send message to bot
    payload={
        'BotID': BotID,
        'LanguageCode': LanguageCode,
        'ConversationID': ConversationID,
        'MessageType': MessageType,
        'ResponseType': ResponseType,
        'TextMsg': TextMsg
    }
    headers = {"Authorization": "Bearer {}".format(IdToken)}
    response = requests.request("POST", sendMessageUrl, headers=headers, data=payload).text
    return response


if __name__ == "__main__":
    app.debug = True
    app.run(port='5001')