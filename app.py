# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('14dw+yTwop0eqsDR5ZTu2RLYuEjNQ3XyyysDXm10czAIi+/Sr9j4cwV9gWeVGkKOVKJ3ZYhd2BukqrM76sfKXDc6mczjnYpn0hYqMR1JgWJQqsVaUBg1+9PPIQOBAfm55jSqynKCehkjYBUbShuengdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('d6823f49d342f709ad7ae25b90674152')

line_bot_api.push_message('U4492871599fb3e554d18bdb13adcdbbb', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('推薦電影',message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='這是推薦電影',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/5zhmdgr.jpg',
                        action=PostbackAction(
                            label='《音速小子3》',
                            display_text='上映日期：2024年12月27日',
                            data='action=001'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/7Kr6EEr.jpg',
                        action=PostbackAction(
                            label='《劇場版「進擊的巨人」完結篇THE LAST ATTACK》',
                            display_text='上映日期：2025年1月03日',
                            data='action=002'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
