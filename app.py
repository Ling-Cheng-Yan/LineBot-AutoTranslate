from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from googletrans import Translator

app = Flask(__name__)

line_bot_api = LineBotApi('Mk3JM2EGziWskG60IBtQ64JQyEkwWucSt6I38g5PpeJM8OTYlzWYODYWRD5FICPBL68PdWsPjBYqWaLRtQ5FViFcd1MvvttZMCmVla2IDyk+gOyjzNkMegltx/HnowO2HhDHg4GsY9kO/XD6kCYqrQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('11bb4dc45040d6321217826fd92f1f62')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

translator = Translator()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    language = translator.detect(msg)
    if 'lang=ja' in language:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=translator.translate(msg, dest='en')))
    elif 'lang=zh-tw' in language:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=translator.translate(msg, dest='en')))
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))

if __name__ == "__main__":
    app.run()