import requests as r
import json
import numpy as np
import datetime

headers = {'X-Yandex-API-Key': 'f480621b-49f1-4b2f-9843-887f382bb864'}
apiKey = 'c053d5ae05234ab2a5b1adb9d9157932'


def get_breez_current(lat, lon):
    res = r.get('https://api.breezometer.com/weather/v1/current-conditions?', params={
        'lat': lat, 'lon': lon, 'key': apiKey
    })
    try:
        return res.json()
    except:
        return 'error'


def get_breez_forecast(lat, lon, hours):
    res = r.get('https://api.breezometer.com/weather/v1/forecast/hourly?', params={
        'lat': lat, 'lon': lon, 'key': apiKey, 'hours': hours
    })
    try:
        return res.json()
    except:
        return 'error'


def get_yandex_current(lat, lon):
    res = r.get('https://api.weather.yandex.ru/v2/forecast', headers=headers, params={
        'lat': lat, 'lon': lon, 'limit': 2, 'hours': True
    })
    try:
        date = res.json()
        pogoda = list([date['forecasts'][0]['hours'], date['forecasts'][1]['hours']])
        now_hour = datetime.datetime.now().hour
        arr = pogoda[0][now_hour:] + pogoda[1][:now_hour]
        return arr
    except:
        return 'error'


# pogoda = get_yandex_current(55.755819, 37.617644)
# print(pogoda)








