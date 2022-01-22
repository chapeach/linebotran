from flask import Flask, request
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from linebot.exceptions import (InvalidSignatureError)
import pandas as pd
import random

app = Flask(__name__)


@app.route("/")
def index():
    return 'line bot ran'


line_bot_api = LineBotApi('239Nfdlzdog9Sxgv/+wgktJPT1Qv9v5Y2oYgVcZkyefEUqqZP5glXKEneFJx+NbH3igLmfjYzssPoaNnzIOAc2lGQcPpx04VRMqSb7qF9MqbnLlpp6vCtHU6aXZ2pGxZwdD+8qHSoi4YhuENXYjG3wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c8b6b3c6cd8160b35da56fe705893ba6')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return
        #print("Invalid signature. Please check your channel access token/channel secret.")
        #abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    msgIn = event.message.text
    msgIn = msgIn.upper()

    print("_"*50)
    print('msg in = ', msgIn)
    userIDline = event.source
    userIDline = str(userIDline)
    print(userIDline)

    targetID = '{"type": "user", "userId": "U1022436d6f4423f7b28e523ecc686e5d"}' #ID line Nesic 2
    targetID = '{"groupId": "C2216d4bf0d2a09b35789de0f73ecced8", "type": "group", "userId": "U2e845bc0d067d47ebcc09ccd540e4a20"}' #ID line pram ในกลุ่ม ran

    if msgIn[0:4] == "RAN." and len(msgIn) == 11:
        df = pd.read_csv("db_site_dtac.csv")

        try:
            findDF = df[df["SiteCode"] == msgIn[4:11]]
            
            siteCode = list(findDF["SiteCode"])[0]
            siteName = list(findDF["SiteName"])[0]
            latLong = list(findDF["LatLong"])[0]
            towerOwner = list(findDF["TowerOwner"])[0]
            towerType = list(findDF["TowerType"])[0]
            fSO = list(findDF["FSO"])[0]

            msgOut = "Site Code : " + siteCode
            msgOut = msgOut + "\nSite Name : " + siteName
            msgOut = msgOut + "\nLat Long : " + latLong
            msgOut = msgOut + "\nTower Owner : " + towerOwner
            msgOut = msgOut + "\nTower Type : " + towerType
            msgOut = msgOut + "\nFSO : " + fSO

            if targetID == userIDline:
                answerMsgOut = ['ไม่บอก','ถามอะไรหนักหนา','ควยเปรม','จำเป็นต้องบอกไหม','อยากใส่เดี่ยวกับเปรม','งัดหน้าแม่ง']
                msgOut = random.choice(answerMsgOut)

        except:
            #print("Error")
            return "Error"

        #print("_"*50)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msgOut))
        print("_"*50)
        print(msgOut)
        print("_"*50)


#if __name__ == "__main__":
#    app.run(debug=True,port=8000)