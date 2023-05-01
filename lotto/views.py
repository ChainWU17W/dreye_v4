from django.shortcuts import render
from django.http import HttpResponse
import random


def index(request):
    return HttpResponse("linebotYOOOOOOOOOOOOOOOOOOOOOOO---lotto!")

# 產生lotto


def get_lotto(request, count=6):
    lottos = []
    while True:
        x = random.randint(1, 49)
        if x not in lottos:
            lottos.append(x)
        if len(lottos) == count:
            break
    lottos.sort()
    lottos.append(random.randint(1, 49))  # 特別號
    result = ','.join(map(str, lottos[:-1]))+f'特別號:{lottos[-1]}'  # 特別號另外處理
    # print(lottos)

    return HttpResponse(result)


# 測試輸出
# print(get_lotto())
