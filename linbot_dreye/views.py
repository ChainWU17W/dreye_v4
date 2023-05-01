from django.http import HttpResponse
from linebot.models import MessageEvent, TextSendMessage
from django.shortcuts import render, HttpResponse


from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

# 爬蟲套件
import requests
from bs4 import BeautifulSoup

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)

# 爬蟲程式寫在callback外即可


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        # -----------------------------------------------------------起手式

        for event in events:
            if isinstance(event, MessageEvent):

                text = event.message.text
                text = text.lower()  # 網址大寫會出錯
                url = f'https://yun.dreye.com/dict_new/dict.php?w={text}&hidden_codepage=01'
                datas = ''
                try:
                    resp = requests.get(url)
                    soup = BeautifulSoup(resp.text, 'lxml')
                    dicts = soup.find(id="infotab1").find_all(
                        'div', class_="sg block")
                    tran = dicts[0].find('ol').find_all('li')
                    # print(tran)  # debug

                    if tran is None:
                        datas = '無法辨識此單字, 請再次確認'
                    else:
                        for i in range(len(tran)):
                            datas += f"【{i+1}】{tran[i].text.strip()} \n"
                    print(datas)

                except Exception as e:
                    print(e)

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=datas)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# -------------------------------------------------------------------------------


def index(request):
    return HttpResponse("my dict!")
