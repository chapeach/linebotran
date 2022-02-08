import re
from flask import Flask, request
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from linebot.exceptions import (InvalidSignatureError)
import pandas as pd


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
def handleMessage(event):

    message_in = event.message.text
    message_in = message_in.upper()

    print("_"*50)
    print('message in = ', message_in)
    user_id_line = event.source
    user_id_line = str(user_id_line)
    print(user_id_line)

    target_id_pram = '{"groupId": "C2216d4bf0d2a09b35789de0f73ecced8", "type": "group", "userId": "U2e845bc0d067d47ebcc09ccd540e4a20"}'
    target_id_bee = '{"groupId": "C2216d4bf0d2a09b35789de0f73ecced8", "type": "group", "userId": "U25f07ed87feb94875314f72faa6e64d6"}'
    target_id_nesic2 = '{"type": "user", "userId": "U1022436d6f4423f7b28e523ecc686e5d"}'
    
    def get_detail_ran():
        try:
            df = pd.read_csv("db_site_dtac.csv")
            find_DF = df[df["SiteCode"] == message_in[4:11]]
            
            siteCode = list(find_DF["SiteCode"])[0]
            siteName = list(find_DF["SiteName"])[0]
            latLong = list(find_DF["LatLong"])[0]
            towerOwner = list(find_DF["TowerOwner"])[0]
            towerType = list(find_DF["TowerType"])[0]
            fSO = list(find_DF["FSO"])[0]

            message_out = "Site Code : " + siteCode
            message_out = message_out + "\nSite Name : " + siteName
            message_out = message_out + "\nLat Long : " + latLong
            message_out = message_out + "\nTower Owner : " + towerOwner
            message_out = message_out + "\nTower Type : " + towerType
            message_out = message_out + "\nFSO : " + fSO

            line_bot_api.reply_message(event.reply_token,TextSendMessage(message_out))
            print("_"*50)
            print(message_out)
            print("_"*50)

        except:
            return "Error"


    def msg_out(message_out):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message_out))
        print("_"*50)
        print(message_out)
        print("_"*50)


    if message_in[0:4] == "RAN." and len(message_in) == 11:
        get_detail_ran()

    
    elif message_in == 'เทสๆ':
        msg_out('ดีจ้า')


    else:
        return


#if __name__ == "__main__":
#    app.run(debug=True,port=5000)