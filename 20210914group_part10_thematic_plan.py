import configparser
from flask import Flask, request, abort
import pandas as pd
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
usertext=['htmldata','csvdata','xlsxdata','analysiscsv']
userdict={'usertext':usertext}
utdf=pd.DataFrame(userdict)

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print(body)
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    
    # 最後須完成進度，將檔案壓縮並郵寄
    
    if event.message.text=='2021AIRC':event.message.text='https://reurl.cc/5245VR'
    elif event.message.text=='motcmpb':
        from sele_motcmpb import selemotcmpbcsv
        selemotcmpbcsv()
        event.message.text='已將motcmpb爬蟲結束!!!'
    elif sum(utdf.values==event.message.text)==1:
        from motcmpbfiles import motcmpbzipfiles
        filesnames=event.message.text
        motcmpbzipfiles(filesnames)
        event.message.text='已寄送使用者搜尋所需壓縮檔'
        
    else:event.message.text='未先執行motcmpb爬蟲指令\n或是沒有此項功能'
    # event.message.text='Suba~Suba~Suba~~~\nWAH~WAH~WAH~~~\nA~Shark~~~\nPE↗KO↘PE↗KO↘~~~\nHA↗HA↘HA↗HA↘~~~'
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()