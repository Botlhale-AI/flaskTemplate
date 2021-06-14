from flask import Flask, render_template, request, session, jsonify, make_response
import requests
import json

app = Flask(__name__)
app.secret_key = 'any random string'

# API Endpoints
generateAuthTokenUrl = "https://dev-botlhale.io/generateAuthToken"
connectUrl = "https://dev-botlhale.io/connect"
sendMessageUrl = "https://dev-botlhale.io/message"

# Chatbot Constants
BotID = "MCAEZWKMLLDMAJYR"
refreshToken = "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.aid6bIFipOODVVlRUKEBibb0bbIlxN9Mut0658ZDVYoDsV_Yrcy8BXXuQT2TZbYKkNIeU0uB7ySRCvFzBB22gibWNZevJmbg4rBbWYiHArPMYxTZcr3UzOq7eBT4bH_XqNRYTiAcEeYU8q0zpZXQMgkMJOGy2HHpoJnJ7ViCawUzSiIa3-EIQwOk7E0ieoGHT95wraMXJqG81zj_uhzTcNU3LyT2u6UGkoL22L61Fp9c9zCBa-KF11OXQ17to03Wtgbcf7X-WBx4as-DKRVANO9Npclo4Qv1-X7C0GXjZKdLiw-5GIKAT1oC75rx-dZVsC710_bEJ9H5CewskKtogQ.czgCmXGxKH4Qb0rt.tAI_Bv8XVEmpUWhaI1E_M1xvtwzwK1iq865eHbRg84flRhV1S3wcL6dSMgBPMCD4kq13dHnBWwsv3zljPsVfjNUFcosRRRa9NcAFBh9KcBu5e0W9LyBYJ7iccvKn8-kGrnXeaaykjYXs0t3uGOZiibMf474R3kacqhrX05_y2cMEOATnDwPgkTTJSSHSycj-4Eutj6rs67C4V2IG2q-f0k0rcY-EIVjK6GajMcrBnShkvewBBQu-R02MQDN-mp8rPZgfI-dGgHqi7vmZs1fa5uUmQjfZIgiswjQQSV2CWx_sFk8DPWf1FiFAfbq8Rav5vWr_cpxc02Tzv8nCW9epxQKrTIMOzhvZjnaTDOSSiVtOxcMc_kLBdsGLmho9DPFxsOcOB08AQ_M4hwe6qOLWB7gRhMiPwwunXvxH5gnBykzKy2X1Wl-VTIGGxnQCCPxNa_e__7rhf8VAa0NKolZ7HLteRqBNTMVeeQEURBMLMQq86lV8KNQY_G0CG3CqivGWwB1TjiD_Fv1Mzu46cd9G-TKZv1rl9KfL-sq_9ghiwGY_Z488iuohdblSzdG9RPEZENIwb3adXQDPR22F9PYyuDHbHrC7jqix-kCbTivuAbVwLizjxzaj4uK1Rj-ipP9r-Ho-J97rwyL1UTpndh8VfVsPmiyAMuk26IXDm32WyigoVGQiKNd5Mpq-c6EZKIhwLycj2wep13RCrrRDJiTNHwKO0tzGNbJC5fxuNKechQ3fPdIfh-p4JgesZEB_1xKBxEIIZyL0J94e4x0cpOed2Flyi3HFI1dRMNJuhoj4_iWAuHFcoNq6VVjEaUe_nKkLGAHO9c1nrzj4rsCDWz7jbSpRYkejA51VeYKIl9T2Da6l-1mJYKGBTOVT0poW8fa4GrxP8hNkwlq-4bPI9snH17UkSV-6dxt96fO4BpDYvEToLYNSkObmYOXJjiMvWDszWEKYKKAJEdOhjyOq0gJ6v0Rf10C5OT2HeIDXUKej2pVQrO9plYICC8uIRJ7aHZIC_5npIZlzXUbBUwD2RAR60FxxEMu4AS4NPudmQsgASIi_w4r_4waAbnrg0zfZB8rIMBthdxM8-FCc7I1mVj7gyKX7rv1lfbyqJDZDjlyy-nSrk5nocz08sCBeLRsFp7cN4W0Q9X4JU70k4Xd8YAPQ00L7Mve6QniHcCXTIEr9TkBSN14mbbD-EtaaOzeTbOIJXKFR6naH6nw0rBklJ9x4XDonf8zG-aeoIBX6LZA3nmI5NvoZX44fUfReI39A-Ezhw22oZwJuFn8ZAPAw3yFep9CYlBSZehDTwGt_wdPzoto93Nr4DoPL-xiTW0Q.1jXqKSqBXVwSEyolJycvyQ"


botName="Mike"
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


# Could be dynamic
LanguageCode = "English"
MessageType = "text"
ResponseType = "text"

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html', botName=botName, firstMessage=firstBotMessage)

@app.route('/startConversation')
def startConversation():
    # Generate Auth Token
    payload={
        'REFRESH_TOKEN': refreshToken,
        }
    IdToken = json.loads(requests.request("POST", generateAuthTokenUrl, data=payload).content)['AuthenticationResult']['IdToken']

    # Generate ConversationID
    payload={
        'BotID': BotID,
        'LanguageCode': LanguageCode
        }
    headers = {"Authorization": "Bearer {}".format(IdToken)}
    ConversationID = json.loads(requests.request("POST", connectUrl, headers=headers, data=payload).content)['ConversationID']

    # Store ConversationID & IdToken for the session
    session['ConversationID'] = ConversationID
    session['IdToken'] = IdToken

    return make_response(jsonify({"ConversationID":ConversationID, "IdToken":IdToken}), 200)

@app.route('/sendMessage', methods = ['GET'])
def sendMessage():
    # Get session variables
    ConversationID = session['ConversationID']
    IdToken = session['IdToken']

    # Get request parameters
    # LanguageCode = request.form.get('LanguageCode')
    # MessageType = request.form.get('MessageType')
    # ResponseType = request.form.get('ResponseType')
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
    app.run(port='5000')