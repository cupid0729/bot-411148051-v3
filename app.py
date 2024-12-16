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
    if re.match('推薦景點',message):
        carousel_template_message = TemplateSendMessage(
            alt_text='熱門旅行景點',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/NBcRFV9.jpg',
                        title='台中',
                        text='taichung',
                        actions=[
                            MessageAction(
                                label='熱門景點',
                                text='國家歌劇院、逢甲夜市、彩虹眷村...'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://zh.wikipedia.org/zh-tw/%E8%87%BA%E4%B8%AD%E5%B8%82'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/3VKcm38.png',
                        title='台北',
                        text='taipei',
                        actions=[
                            MessageAction(
                                label='熱門景點',
                                text='木柵動物園、台北101、故宮博物院...'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://www.travel.taipei/zh-tw'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/0r69scM.png',
                        title='高雄',
                        text='Kaohsiung',
                        actions=[
                            MessageAction(
                                label='熱門景點',
                                text='瑞豐夜市、科學工藝博物館、愛河...'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://www.welcometw.com/%E9%AB%98%E9%9B%84%E6%99%AF%E9%BB%9E%E6%8E%A8%E8%96%A6-%EF%BD%9C%E9%AB%98%E9%9B%84%E6%9C%80%E7%BE%8E%E6%9C%80%E5%A4%AFig%E6%89%93%E5%8D%A1%E6%99%AF%E9%BB%9E%EF%BC%8C%E5%B8%82%E5%8D%80%E3%80%81/'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
