import pandas as pd
import tensorflow.keras as K
import tensorflow.keras.layers as L
from tensorflow.keras.models import Sequential as M
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.losses import categorical_crossentropy, binary_crossentropy
import numpy as np
import datetime
from django.conf import settings
import businesscard.weather as weather
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
import threading
from django.views.generic import CreateView
from .forms import AddPostForm
from django.shortcuts import render
import os
from django.http import JsonResponse
from .models import *

PDK_CO = 5
PDK_NO = 0.4
PDK_NO2 = 0.2
PDK_MP10 = 0.3
PDK_MP25 = 0.16


def predict_CO_6(x): # предсказание СО на 6 часов 
    model = K.models.load_model('LCTmodels/COAllNoTest6HoursSeq1.h5') # подключение модели
    pred = model.predict(x) # предсказание
    return round(pred[0][0], 2) # возврат значение


def predict_NO_6(x): # предсказание NO на 6 часов 
    model = K.models.load_model('LCTmodels/NOMeteoNoTest6HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_NO2_6(x): # предсказание NO2 на 6 часов   (аналогично предыдущим)
    model = K.models.load_model('LCTmodels/NO2MeteoNoTest6HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_MP10_6(x): # предсказание PM10 на 6 часов 
    model = K.models.load_model('LCTmodels/PM10MeteoNoTest6HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_MP25_6(x): # предсказание PM2.5 на 6 часов 
    model = K.models.load_model('LCTmodels/PM25AllNoTest6HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_CO_3(x):  # предсказание CO на 3 часов 
    model = K.models.load_model('LCTmodels/COAllNoTest3HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_NO_3(x): # предсказание NO на 3 часов 
    model = K.models.load_model('LCTmodels/NOAllNoTest3HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_NO2_3(x): # предсказание NO2 на 3 часов 
    model = K.models.load_model('LCTmodels/NO2MeteoNoTest3HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_MP10_3(x): # предсказание PM10 на 3 часов 
    model = K.models.load_model('LCTmodels/PM10MeteoNoTest3HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_MP25_3(x): # предсказание PM2.5 на 3 часов 
    model = K.models.load_model('LCTmodels/PM25AllNoTest3HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_CO_1(x): # предсказание CO на 1 часов 
    model = K.models.load_model('LCTmodels/COAllNoTest1HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_NO_1(x): # предсказание NO на 1 часов 
    model = K.models.load_model('LCTmodels/NOMeteoNoTest1HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_NO2_1(x): # предсказание NO2 на 1 часов
    model = K.models.load_model('LCTmodels/NO2MeteoNoTest1HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_MP10_1(x): # предсказание PM10 на 1 часов
    model = K.models.load_model('LCTmodels/PM10AllNoTest1HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_MP25_1(x): # предсказание PM2.5 на 1 часов
    model = K.models.load_model('LCTmodels/PM25MeteoNoTest1HoursSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_CO(x): # предсказание CO на 20 минут
    model = K.models.load_model('LCTmodels/COMeteoNoTestSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_NO(x): # предсказание NO на 20 минут
    model = K.models.load_model('LCTmodels/NOAllnoTestSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_NO2(x): # предсказание NO2 на 20 минут
    model = K.models.load_model('LCTmodels/NO2AllNoTestSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_MP10(x): # предсказание PM10 на 20 минут
    model = K.models.load_model('LCTmodels/PM10MeteoNoTestSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_MP25(x): # предсказание PM2.5 на 20 минут
    model = K.models.load_model('LCTmodels/PM25MeteoNotestSeq1.h5')
    pred = model.predict(x)
    return round(pred[0][0], 2)


def predict_quality(obj): # функция паредсказания всех элементов на 20 минут исходя из последних данных
    predCO = predict_CO([[[obj.temp, obj.speed, obj.direction, obj.pressure, obj.humidity,  # придсказаниие CO
                           obj.precipitation, obj.CO]]])
    predNO = predict_NO([[[obj.CO, obj.NO2, obj.NO, obj.temp, obj.speed, obj.direction, obj.pressure, obj.humidity,   # придсказаниие NO
                           obj.precipitation]]])
    predNO2 = predict_NO2([[[obj.CO, obj.NO2, obj.NO, obj.temp, obj.speed, obj.direction, obj.pressure, obj.humidity,   # придсказаниие NO2
                             obj.precipitation]]])
    predNMP10 = predict_MP10([[[obj.temp, obj.speed, obj.direction, obj.pressure,    # придсказаниие PM10
                                obj.humidity, obj.precipitation, obj.MP10]]])
    predNMP25 = predict_MP25([[[obj.temp, obj.speed, obj.direction, obj.pressure,    # придсказаниие PM2.5
                                obj.humidity, obj.precipitation, obj.MP25]]])
    return [predCO, predNO, predNO2, predNMP10, predNMP25]


def createPolygon(data, prop={}):   # функция создание объекта полигона для geojson
    pt = dict()
    pt["type"] = "Feature"
    pt["properties"] = prop
    pt["geometry"] = dict()
    pt["geometry"]["type"] = "LineString"
    pt["geometry"]["coordinates"] = data
    return pt


def createLine(data, prop={}):  # функция создание объекта линия для geojson
    pt = dict()
    pt["type"] = "Feature"
    pt["properties"] = prop
    pt["geometry"] = dict()
    pt["geometry"]["type"] = "LineString"
    pt["geometry"]["coordinates"] = data
    return pt


def createPoint(data, prop={}):  # функция создание объекта точки для geojson
    pt = dict()
    pt["type"] = "Feature"
    pt["properties"] = prop
    pt["geometry"] = dict()
    pt["geometry"]["type"] = "Point"
    pt["geometry"]["coordinates"] = data
    return pt


def createLayer(data, prop={}):  # функция создание объекта слоя для geojson
    geojson = dict()
    geojson["type"] = "FeatureCollection"
    geojson["properties"] = prop
    geojson["features"] = data
    return geojson


def mean_quality(CO, NO, NO2, PM10, PM25):  # подсчет среднего качетсва воздуха относительно ПДК
    return round(CO / PDK_CO + NO / PDK_NO + NO2 / PDK_NO2 + PM10 / PDK_MP10 + PM25 / PDK_MP25, 2)


def get_tower(request):  # функция создания слоя geojson со станциями
    data = list()
    for i in Station.objects.all():
        if Data.objects.filter(station=i):
            d = Data.objects.filter(station=i).order_by('date').last()
            pred_data = predict_quality(d)
            mean_qual = mean_quality(d.CO, d.NO, d.NO2, d.MP10, d.MP25)
            html = render(request, 'popus.html',
                          context={'title': i.name, 'NO': d.NO, "NO2": d.NO2, "CO": d.CO, "MP10": d.MP10,
                                   'mean_qual': mean_qual,
                                   'MP25': d.MP25, 'no': 0, 'id': i.pk, 'pred': pred_data}).content.decode('utf-8')
            data.append(createPoint([i.lon, i.lat],
                                    {'title': i.name, 'NO': d.NO, "NO2": d.NO2, "CO": d.CO, "MP10": d.MP10,
                                     'MP25': d.MP25, 'no': 0, 'html': html, 'id': i.pk}))
        else:
            html = render(request, 'popus.html', context={'title': i.name, 'NO': 0, "NO2": 0, "CO": 0, "MP10": 0,
                                                          'MP25': 0, 'no': 1, 'id': i.pk}).content.decode('utf-8')
            data.append(createPoint([i.lon, i.lat],
                                    {'title': i.name, 'NO': 0, "NO2": 0, "CO": 0, "MP10": 0,
                                     'MP25': 0, 'no': 1, 'html': html, 'id': i.pk}))
    tower = createLayer(data)
    return tower


def get_prom():   # функция создания слоя geojson с промышленностью
    data = list()
    for i in Industry.objects.all():
        data.append(
            createPoint([i.lon, i.lat],
                        {'title': i.name, 'discript': i.address, 'ind': i.index, 'phone': i.phone, 'email': i.email,
                         'id': i.id}))
    prom = createLayer(data)
    return prom


def get_build():  # функция создания слоя geojson со стройками
    data = list()
    for i in Building.objects.all()[:250]:
        data.append(
            createPoint([i.lon, i.lat], {'title': i.name, 'address': i.address, 'end_year': i.end_year, 'url': i.url}))
    build = createLayer(data)
    return build


def map(request):   # функция рендеринга страницы "Карта контроля"
    # [долгота, широта]

    prom = get_prom()   # получения словаря (слоя с промышленностью)

    build = get_build()   # получения словаря (слоя со стройками)

    tower = get_tower(request)  # получения словаря (слоя со станциями)

    return render(request, "index.html", {'data': tower, 'prom': prom, 'build': build})


def statistics(request):   # функция рендеринга страницы "Статистика"
    label = list()
    CO = list()
    NO = list()
    NO2 = list()
    PM10 = list()
    PM25 = list()
    industry = Industry.objects.all()  # получений всех объектов промышленности
    for s in Station.objects.all():   # перебор станций
        data = Data.objects.filter(station=s).order_by('date').last()  # получение последних данных станции
        label.append(s.name)
        CO.append(data.CO)
        NO.append(data.NO)
        NO2.append(data.NO2)
        PM10.append(data.MP10)
        PM25.append(data.MP25)
    data = weather.get_breez_current(55.755819, 37.617644)['data'] # получение погоды
    return render(request, "statistics.html",
                  {'ind': industry, 'data': data, 'label': label, 'co': CO, 'no': NO, 'no2': NO2, 'pm10': PM10,
                   'pm25': PM25})


def get_weather_hour(pogoda, now, next_time):  # функция получения погоды на определенный час
    time = now + datetime.timedelta(minutes=next_time)
    if time.minute > 30:
        time = time + datetime.timedelta(hours=1)
        hour = time.hour
    else:
        hour = time.hour
    pogoda_hour = pogoda[hour - now.hour]
    return pogoda_hour


def set_false(name, station):  # функция вызывается в случае отсутствия данных на станции по которым можно делать прогноз
    pred = Prediction.objects.filter(name=name, station=station).first()
    if pred:
        pred.CO = 0
        pred.NO = 0
        pred.NO2 = 0
        pred.MP10 = 0
        pred.MP25 = 0
        pred.save()
    else:
        Prediction.objects.create(name=name, station=station, CO=0, NO=0, NO2=0, MP10=0, MP25=0).save()


def all_predict():  # функция предсказания данных
    now = datetime.datetime.now()
    timeline = ['+00:20', '+00:40', '+01:00', '+01:20', '+01:40', '+02:00', '+02:20', '+02:40', '+03:00', '+03:20',
                '+03:40',
                '+04:00', '+04:20', '+04:40', '+05:00', '+05:20', '+05:40', '+06:00', '+06:20', '+06:40', '+07:00',
                '+07:20',
                '+07:40', '+08:00', '+08:20', '+08:40', '+09:00', '+09:20', '+09:40', '+10:00', '+10:20', '+10:40',
                '+11:00',
                '+11:20', '+11:40', '+12:00', '+12:20', '+12:40', '+13:00', '+13:20', '+13:40', '+14:00', '+14:20',
                '+14:40',
                '+15:00', '+15:20', '+15:40', '+16:00', '+16:20', '+16:40', '+17:00', '+17:20', '+17:40', '+18:00',
                '+18:20',
                '+18:40', '+19:00', '+19:20', '+19:40', '+20:00', '+20:20', '+20:40', '+21:00', '+21:20', '+21:40',
                '+22:00',
                '+22:20', '+22:40', '+23:00', '+23:20', '+23:40', '+24:00']
    for s in Station.objects.all():
        pogoda = weather.get_breez_forecast(lat=s.lat, lon=s.lon, hours=26)['data'][2:]  # получение прогноза погоды на различных станциях на 24 часа вперед
        for ind, name in enumerate(timeline, start=1):
            first_pred = False
            not_fail = True
            delta = ind * 20
            next_time = 0
            while delta > 0:
                if delta >= 360:
                    delta -= 360
                    pogoda_hour = get_weather_hour(pogoda, now, next_time)
                    next_time += 360
                    if not first_pred:  # предсказание хим элементов в случае 1 прогноза на 6 часов
                        data = Data.objects.filter(station=s).order_by('date').last()
                        if data:
                            predCO = predict_CO_6(np.array([[[data.temp, data.speed,
                                                              data.direction, data.pressure, data.humidity,
                                                              data.precipitation, data.CO]]]))
                            predNO = predict_NO_6(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                              data.humidity, data.precipitation, data.NO]]]))
                            predNO2 = predict_NO2_6(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                                data.humidity, data.precipitation, data.NO2]]]))
                            predMP10 = predict_MP10_6(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                                  data.humidity, data.precipitation, data.MP10]]]))
                            predMP25 = predict_MP25_6(np.array([[[data.temp, data.speed,
                                                                  data.direction, data.pressure, data.humidity,
                                                                  data.precipitation, data.MP25]]]))
                            predCO = round(predCO, 2)
                            predNO = round(predNO, 2)
                            predNO2 = round(predNO2, 2)
                            predMP10 = round(predMP10, 2)
                            predMP25 = round(predMP25, 2)
                        else:
                            set_false(name, s)
                            not_fail = False
                            break
                        first_pred = True
                    else:     # предсказание хим элементов на 6 часов
                        predCO1 = predict_CO_6(np.array([[[pogoda_hour['temperature']['value'],
                                                           round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                           pogoda_hour['wind']['direction'],
                                                           round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                           pogoda_hour['relative_humidity'],
                                                           pogoda_hour['precipitation']['total_precipitation'][
                                                               'value'], predCO]]]))
                        predNO1 = predict_NO_6(np.array([[[pogoda_hour['temperature']['value'],
                                                           round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                           pogoda_hour['wind']['direction'],
                                                           round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                           pogoda_hour['relative_humidity'],
                                                           pogoda_hour['precipitation']['total_precipitation']['value'],
                                                           predNO]]]))
                        predNO21 = predict_NO2_6(np.array([[[pogoda_hour['temperature']['value'],
                                                             round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                             pogoda_hour['wind']['direction'],
                                                             round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                             pogoda_hour['relative_humidity'],
                                                             pogoda_hour['precipitation']['total_precipitation'][
                                                                 'value'],
                                                             predNO2]]]))
                        predMP101 = predict_MP10_6(np.array([[[pogoda_hour['temperature']['value'],
                                                               round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                               pogoda_hour['wind']['direction'],
                                                               round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                               pogoda_hour['relative_humidity'],
                                                               pogoda_hour['precipitation']['total_precipitation'][
                                                                   'value'], predMP10]]]))
                        predMP251 = predict_MP25_6(
                            np.array([[[pogoda_hour['temperature']['value'],
                                        round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                        pogoda_hour['wind']['direction'],
                                        round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                        pogoda_hour['relative_humidity'],
                                        pogoda_hour['precipitation']['total_precipitation'][
                                            'value'], predMP25]]]))
                        predCO = round(predCO1, 2)
                        predNO = round(predNO1, 2)
                        predNO2 = round(predNO21, 2)
                        predMP10 = round(predMP101, 2)
                        predMP25 = round(predMP251, 2)

                elif delta >= 180:
                    delta -= 180
                    pogoda_hour = get_weather_hour(pogoda, now, next_time)
                    next_time += 180
                    if not first_pred:
                        data = Data.objects.filter(station=s).order_by('date').last()
                        if data:                           # предсказание хим элементов в случае 1 прогноза на 3 часа
                            predCO = predict_CO_3(np.array([[[data.temp, data.speed,
                                                              data.direction, data.pressure, data.humidity,
                                                              data.precipitation, predCO]]]))
                            predNO = predict_NO_3(np.array([[[data.temp, data.speed,
                                                              data.direction, data.pressure, data.humidity,
                                                              data.precipitation, data.NO]]]))
                            predNO2 = predict_NO2_3(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                                data.humidity, data.precipitation, data.NO2]]]))
                            predMP10 = predict_MP10_3(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                                  data.humidity, data.precipitation, data.MP10]]]))
                            predMP25 = predict_MP25_3(np.array([[[data.temp, data.speed,
                                                                  data.direction, data.pressure, data.humidity,
                                                                  data.precipitation, data.MP25]]]))
                            predCO = round(predCO, 2)
                            predNO = round(predNO, 2)
                            predNO2 = round(predNO2, 2)
                            predMP10 = round(predMP10, 2)
                            predMP25 = round(predMP25, 2)
                        else:
                            set_false(name, s)
                            not_fail = False
                            break
                        first_pred = True
                    else:      # предсказание хим элементов на 3 часа
                        predCO1 = predict_CO_3(np.array([[[pogoda_hour['temperature']['value'],
                                                           round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                           pogoda_hour['wind']['direction'],
                                                           round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                           pogoda_hour['relative_humidity'],
                                                           pogoda_hour['precipitation']['total_precipitation'][
                                                               'value'], predCO]]]))
                        predNO1 = predict_NO_3(np.array([[[pogoda_hour['temperature']['value'],
                                                           round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                           pogoda_hour['wind']['direction'],
                                                           round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                           pogoda_hour['relative_humidity'],
                                                           pogoda_hour['precipitation']['total_precipitation'][
                                                               'value'], predNO]]]))
                        predNO21 = predict_NO2_3(np.array([[[pogoda_hour['temperature']['value'],
                                                             round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                             pogoda_hour['wind']['direction'],
                                                             round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                             pogoda_hour['relative_humidity'],
                                                             pogoda_hour['precipitation']['total_precipitation'][
                                                                 'value'],
                                                             predNO2]]]))
                        predMP101 = predict_MP10_3(np.array([[[pogoda_hour['temperature']['value'],
                                                               round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                               pogoda_hour['wind']['direction'],
                                                               round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                               pogoda_hour['relative_humidity'],
                                                               pogoda_hour['precipitation']['total_precipitation'][
                                                                   'value'], predMP10]]]))
                        predMP251 = predict_MP25_3(
                            np.array([[[pogoda_hour['temperature']['value'],
                                        round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                        pogoda_hour['wind']['direction'],
                                        round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                        pogoda_hour['relative_humidity'],
                                        pogoda_hour['precipitation']['total_precipitation'][
                                            'value'], predMP25]]]))
                        predCO = round(predCO1, 2)
                        predNO = round(predNO1, 2)
                        predNO2 = round(predNO21, 2)
                        predMP10 = round(predMP101, 2)
                        predMP25 = round(predMP251, 2)
                elif delta >= 60:
                    delta -= 60
                    pogoda_hour = get_weather_hour(pogoda, now, next_time)
                    next_time += 60
                    if not first_pred:
                        data = Data.objects.filter(station=s).order_by('date').last()
                        if data:                                # предсказание хим элементов в случае 1 прогноза на 1 час
                            predCO = predict_CO_1(np.array([[[data.temp, data.speed,
                                                              data.direction, data.pressure, data.humidity,
                                                              data.precipitation, data.CO]]]))
                            predNO = predict_NO_1(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                              data.humidity, data.precipitation, data.NO]]]))
                            predNO2 = predict_NO2_1(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                                data.humidity, data.precipitation, data.NO2]]]))
                            predMP10 = predict_MP10_1(np.array([[[data.temp, data.speed,
                                                                  data.direction, data.pressure, data.humidity,
                                                                  data.precipitation, data.MP10]]]))
                            predMP25 = predict_MP25_1(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                                  data.humidity, data.precipitation, data.MP25]]]))
                            predCO = round(predCO, 2)
                            predNO = round(predNO, 2)
                            predNO2 = round(predNO2, 2)
                            predMP10 = round(predMP10, 2)
                            predMP25 = round(predMP25, 2)
                        else:
                            set_false(name, s)
                            not_fail = False
                            break
                        first_pred = True
                    else:                # предсказание хим элементов на 1 час
                        predCO1 = predict_CO_1(np.array([[[pogoda_hour['temperature']['value'],
                                                           round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                           pogoda_hour['wind']['direction'],
                                                           round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                           pogoda_hour['relative_humidity'],
                                                           pogoda_hour['precipitation']['total_precipitation'][
                                                               'value'], predCO]]]))
                        predNO1 = predict_NO_1(np.array([[[pogoda_hour['temperature']['value'],
                                                           round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                           pogoda_hour['wind']['direction'],
                                                           round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                           pogoda_hour['relative_humidity'],
                                                           pogoda_hour['precipitation']['total_precipitation']['value'],
                                                           predNO]]]))
                        predNO21 = predict_NO2_1(np.array([[[pogoda_hour['temperature']['value'],
                                                             round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                             pogoda_hour['wind']['direction'],
                                                             round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                             pogoda_hour['relative_humidity'],
                                                             pogoda_hour['precipitation']['total_precipitation'][
                                                                 'value'],
                                                             predNO2]]]))
                        predMP101 = predict_MP10_1(
                            np.array([[[pogoda_hour['temperature']['value'],
                                        round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                        pogoda_hour['wind']['direction'],
                                        round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                        pogoda_hour['relative_humidity'],
                                        pogoda_hour['precipitation']['total_precipitation'][
                                            'value'], predMP10]]]))
                        predMP251 = predict_MP25_1(
                            np.array([[[pogoda_hour['temperature']['value'],
                                        round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                        pogoda_hour['wind']['direction'],
                                        round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                        pogoda_hour['relative_humidity'],
                                        pogoda_hour['precipitation']['total_precipitation'][
                                            'value'], predMP25]]]))
                        predCO = round(predCO1, 2)
                        predNO = round(predNO1, 2)
                        predNO2 = round(predNO21, 2)
                        predMP10 = round(predMP101, 2)
                        predMP25 = round(predMP251, 2)
                elif delta >= 20:
                    delta -= 20
                    pogoda_hour = get_weather_hour(pogoda, now, next_time)
                    next_time += 20
                    if not first_pred:
                        data = Data.objects.filter(station=s).order_by('date').last()
                        if data:                                # предсказание хим элементов в случае 1 прогноза на 20 минут
                            predCO = predict_CO(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                            data.humidity, data.precipitation, data.CO]]]))
                            predNO = predict_NO(np.array([[[data.CO, data.NO2, data.NO, data.temp, data.speed,
                                                            data.direction, data.pressure, data.humidity,
                                                            data.precipitation]]]))
                            predNO2 = predict_NO2(np.array([[[data.CO, data.NO2, data.NO, data.temp, data.speed,
                                                              data.direction, data.pressure, data.humidity,
                                                              data.precipitation]]]))
                            predMP10 = predict_MP10(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                                data.humidity, data.precipitation, data.MP10]]]))
                            predMP25 = predict_MP25(np.array([[[data.temp, data.speed, data.direction, data.pressure,
                                                                data.humidity, data.precipitation, data.MP25]]]))
                            predCO = round(predCO, 2)
                            predNO = round(predNO, 2)
                            predNO2 = round(predNO2, 2)
                            predMP10 = round(predMP10, 2)
                            predMP25 = round(predMP25, 2)
                        else:
                            set_false(name, s)
                            not_fail = False
                            break
                        first_pred = True
                    else:         # предсказание хим элементов на 20 минут
                        predCO1 = predict_CO(np.array([[[pogoda_hour['temperature']['value'],
                                                         round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                         pogoda_hour['wind']['direction'],
                                                         round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                         pogoda_hour['relative_humidity'],
                                                         pogoda_hour['precipitation']['total_precipitation']['value'],
                                                         predCO]]]))
                        predNO1 = predict_NO(np.array([[[predCO, predNO2, predNO, pogoda_hour['temperature']['value'],
                                                         round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                         pogoda_hour['wind']['direction'],
                                                         round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                         pogoda_hour['relative_humidity'],
                                                         pogoda_hour['precipitation']['total_precipitation'][
                                                             'value']]]]))
                        predNO21 = predict_NO2(np.array([[[predCO, predNO2, predNO, pogoda_hour['temperature']['value'],
                                                           round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                                           pogoda_hour['wind']['direction'],
                                                           round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                                           pogoda_hour['relative_humidity'],
                                                           pogoda_hour['precipitation']['total_precipitation'][
                                                               'value']]]]))
                        predMP101 = predict_MP10(
                            np.array([[[pogoda_hour['temperature']['value'],
                                        round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                        pogoda_hour['wind']['direction'],
                                        round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                        pogoda_hour['relative_humidity'],
                                        pogoda_hour['precipitation']['total_precipitation'][
                                            'value'], predMP10]]]))
                        predMP251 = predict_MP25(
                            np.array([[[pogoda_hour['temperature']['value'],
                                        round(pogoda_hour['wind']['speed']['value'] / 3.6, 2),
                                        pogoda_hour['wind']['direction'],
                                        round(pogoda_hour['pressure']['value'] / 1.333, 2),
                                        pogoda_hour['relative_humidity'],
                                        pogoda_hour['precipitation']['total_precipitation'][
                                            'value'], predMP25]]]))
                        predCO = round(predCO1, 2)
                        predNO = round(predNO1, 2)
                        predNO2 = round(predNO21, 2)
                        predMP10 = round(predMP101, 2)
                        predMP25 = round(predMP251, 2)
            if not_fail:             # создание или изменение модели предсказания на определенный час на станции
                pred = Prediction.objects.filter(name=name, station=s).first()
                print(name)
                if pred:
                    pred.CO = round(predCO, 2)
                    pred.NO = round(predNO, 2)
                    pred.NO2 = round(predNO2, 2)
                    pred.MP10 = round(predMP10, 2)
                    pred.MP25 = round(predMP25, 2)
                    pred.save()
                else:
                    Prediction.objects.create(name=name, station=s, CO=round(predCO, 2), NO=round(predNO, 2),
                                              NO2=round(predNO2, 2), MP10=round(predMP10, 2),
                                              MP25=round(predMP25, 2)).save()


def get_tower_for_predict(request):
    data = list()
    for i in Station.objects.all():
        data.append(createPoint([i.lon, i.lat],
                                {'id': i.pk}))
    tower = createLayer(data)
    return tower


def predict(request):   # функция рендеринга страницы "Прогноз"
    # tut dimas skazal ti bomj i need 2 mernyi massiv
    threading.Thread(target=all_predict, args=()).start()
    timeline = ['+00:20', '+00:40', '+01:00', '+01:20', '+01:40', '+02:00', '+02:20', '+02:40', '+03:00', '+03:20',
                '+03:40',
                '+04:00', '+04:20', '+04:40', '+05:00', '+05:20', '+05:40', '+06:00', '+06:20', '+06:40', '+07:00',
                '+07:20',
                '+07:40', '+08:00', '+08:20', '+08:40', '+09:00', '+09:20', '+09:40', '+10:00', '+10:20', '+10:40',
                '+11:00',
                '+11:20', '+11:40', '+12:00', '+12:20', '+12:40', '+13:00', '+13:20', '+13:40', '+14:00', '+14:20',
                '+14:40',
                '+15:00', '+15:20', '+15:40', '+16:00', '+16:20', '+16:40', '+17:00', '+17:20', '+17:40', '+18:00',
                '+18:20',
                '+18:40', '+19:00', '+19:20', '+19:40', '+20:00', '+20:20', '+20:40', '+21:00', '+21:20', '+21:40',
                '+22:00',
                '+22:20', '+22:40', '+23:00', '+23:20', '+23:40', '+24:00']
    timeline_id = list()
    for i in range(len(timeline)):
        timeline_id.append([timeline[i], 'timeline_id_' + str(i)])
    tower = get_tower_for_predict(request)
    print(tower)

    data = {"timeline_id": timeline_id, 'tower': tower}
    return render(request, "predict.html", data)


def nn(size, input_size, out_size=1, type_nn='reg'):    # создание полносвязной модели
    model = M()
    model.add(L.Input(input_size))
    model.add(L.Flatten())
    for i in range(size):
        model.add(L.Dense(pow(2, 9 - i), 'relu'))
    if type_nn == 'reg':
        model.add(L.Dense(out_size, 'linear'))
        model.summary()
        model.compile(optimizer='Adam', loss='mse', metrics=['accuracy'])
    if type_nn == 'classif':
        model.add(L.Dense(out_size, 'softmax'))
        model.summary()
        if out_size == 2:
            model.compile(optimizer='Adam', loss=binary_crossentropy, metrics=['accuracy'])
        else:
            model.compile(optimizer='Adam', loss=categorical_crossentropy, metrics=['accuracy'])
    return model


def rnn(size, input_size, out_size, type_nn='reg'):      # создание рекурентной модели
    model = M()
    model.add(L.Input(input_size))
    for i in range(size - 1):
        model.add(L.LSTM(pow(2, 7 - i), return_sequences=True))
    model.add(L.LSTM(pow(2, 6 - size)))
    model.add(L.Dense(pow(2, 6 - size), 'relu'))
    if type_nn == 'reg':
        model.add(L.Dense(out_size, 'linear'))
        model.summary()
        model.compile(optimizer='Adam', loss='mse', metrics=['accuracy'])
    if type_nn == 'classif':
        model.add(L.Dense(out_size, 'softmax'))
        model.summary()
        if out_size == 2:
            model.compile(optimizer='Adam', loss=binary_crossentropy, metrics=['accuracy'])
        else:
            model.compile(optimizer='Adam', loss=categorical_crossentropy, metrics=['accuracy'])
    return model


def cnn(size, input_size, out_size, type_nn='classif'):     # создание сверточной модели
    model = M()
    model.add(L.Input(input_size))
    for i in range(size):
        if i > 3:
            model.add(L.Conv2D(pow(2, 9), (3, 3), padding='same', activation='relu'))
            model.add(L.MaxPooling2D((2, 2)))
            model.add(L.Dropout(0.3))
        else:
            model.add(L.Conv2D(pow(2, 5 + i), (3, 3), padding='same', activation='relu'))
            model.add(L.MaxPooling2D((2, 2)))
            model.add(L.Dropout(0.3))
    model.add(L.Flatten())
    model.add(L.Dense(64, 'relu'))
    model.add(L.Dense(32, 'relu'))
    if type_nn == 'reg':
        model.add(L.Dense(out_size, 'linear'))
        model.summary()
        model.compile(optimizer='Adam', loss='mse', metrics=['accuracy'])
    if type_nn == 'classif':
        model.add(L.Dense(out_size, 'softmax'))
        model.summary()
        if out_size == 2:
            model.compile(optimizer='Adam', loss=binary_crossentropy, metrics=['accuracy'])
        else:
            model.compile(optimizer='Adam', loss=categorical_crossentropy, metrics=['accuracy'])
    return model


def create_model(request):  # функция рендеринга страницы "Создание модели"
    return render(request, "create_model.html")


def create_file(f):     # сохранение файла данных (признаки или ответы)
    with open(f.name, 'wb') as w:
        w.write(f.read())


def get_data(data):     # получение признаков или ответов
    x_train = list()
    x = np.array(data)
    x = np.expand_dims(x, 1)
    for i in x:
        x_train.append(i)
    return np.array(x_train)


def create_model_ajax(request):   # функция вызываемая запросом ajax для создания и обучения  выбранной кастомной модели модели
    data = dict()
    config = request.POST
    x_file = request.FILES['features']
    y_file = request.FILES['answer']
    create_file(x_file)
    create_file(y_file)
    if x_file.name.split('.')[-1] == 'csv':
        x_train = pd.read_csv(x_file.name)
        x_train = x_train.fillna(0)
    elif (x_file.name.split('.')[-1] == 'xls') or (x_file.name.split('.')[-1] == 'xlsx'):
        x_train = pd.read_excel(x_file.name)
        x_train = x_train.fillna(0)
    if y_file.name.split('.')[-1] == 'csv':
        y_train = pd.read_csv(x_file.name)
    elif (y_file.name.split('.')[-1] == 'xls') or (y_file.name.split('.')[-1] == 'xlsx'):
        y_train = pd.read_excel(y_file.name)
    x_train = x_train[:min(x_train.shape[0], y_train.shape[0])]
    y_train = y_train[:min(x_train.shape[0], y_train.shape[0])]
    if config['out'] == 'reg':
        out_size = 1
        col = y_train.columns[0]
        y_train = np.array(y_train[col])
    else:
        col = y_train.columns[0]
        y_train = np.array(y_train[col])
        y_train = y_train - y_train.min()
        out_size = y_train.max() - y_train.min() + 1
        y_train = to_categorical(y_train, num_classes=out_size)
    x_train = get_data(x_train)
    if config['type'] == 'dff':
        model = nn(int(config['size']), x_train.shape[1:], out_size, type_nn=config['out'])
    elif config['type'] == 'rnn':
        model = rnn(int(config['size']), x_train.shape[1:], out_size, type_nn=config['out'])
    elif config['type'] == 'dnc':
        if len(x_train.shape[1:]) == 2:
            x_train = np.expand_dims(x_train, 3)
        model = cnn(int(config['size']), x_train.shape[1:], out_size, type_nn=config['out'])
    history = model.fit(x_train, y_train, batch_size=32, epochs=5, validation_split=.2)
    _, train_val = model.evaluate(x_train[int(x_train.shape[0] * 0.7):], y_train[int(x_train.shape[0] * 0.7):])
    model.save('maybe.h5')
    data['name'] = 'maybe.h5'
    data['val'] = train_val
    os.remove(x_file.name)
    os.remove(y_file.name)
    return JsonResponse(data)


def save_model(request):
    pass

def cancel_model(request):    # удаление модели
    os.remove('maybe.h5')
    return JsonResponse({'ok': 'ok'})


def docs(request):  # функция рендеринга страницы "Информация"
    return render(request, "docs.html")


def location(request):  # функция рендеринга страницы "Засечь место"
    street = Street.objects.all()
    industry = Industry.objects.all()
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            email_content = render(request, 'email.html').content.decode('utf-8')
            msg = EmailMessage('Заявка', email_content, settings.EMAIL_HOST_USER, [request.POST['email']])    # отправка сообщения заявителю
            msg.content_subtype = 'html'
            msg.send()
            email_content = render(request, 'email_report.html').content.decode('utf-8')
            msg = EmailMessage('Жалоба', email_content, settings.EMAIL_HOST_USER,
                               [Industry.objects.get(id=request.POST['name_industry']).email])
            msg.content_subtype = 'html'
            msg.send()
            return JsonResponse({'ok': "ok"})
        else:
            return render(request, 'location.html', {'street': street, 'industry': industry})
    else:
        return render(request, 'location.html', {'street': street, 'industry': industry})


def get_pred(request):    # ajax запром на получение определенного предсказания
    pred = Prediction.objects.filter(name=request.POST['name'],
                                     station=Station.objects.get(id=int(request.POST['id']))).first()
    return JsonResponse({'co': pred.CO, 'no': pred.NO, 'no2': pred.NO2, 'mp10': pred.MP10, 'mp25': pred.MP25})
