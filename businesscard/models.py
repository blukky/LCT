from django.db import models
from django.db.models import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render


class Station(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название станции")
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'


class Industry(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название промышленного здания")
    index = models.CharField(max_length=10, blank=True, null=True, verbose_name='Индекс')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Адрес')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, null=True, verbose_name='Почта')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Промышленное здание'
        verbose_name_plural = 'Промышленные здания'


class Data(models.Model):  # создание таблицы данных
    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name='Станция')
    NO = models.FloatField(verbose_name='NO', blank=True, null=True)
    NO2 = models.FloatField(verbose_name='NO2', blank=True, null=True)
    CO = models.FloatField(verbose_name='CO', blank=True, null=True)
    MP10 = models.FloatField(verbose_name='MP10', blank=True, null=True)
    MP25 = models.FloatField(verbose_name='MP2.5', blank=True, null=True)
    speed = models.FloatField(verbose_name='Скорость ветра', blank=True, null=True)
    direction = models.FloatField(verbose_name='Направление ветра', blank=True, null=True)
    temp = models.FloatField(verbose_name='Температура', blank=True, null=True)
    pressure = models.FloatField(verbose_name='Давление', blank=True, null=True)
    humidity = models.FloatField(verbose_name='Влажность', blank=True, null=True)
    precipitation = models.FloatField(verbose_name='Осадки', blank=True, null=True)
    date = models.DateTimeField(verbose_name="Дата и время", auto_now=True)

    def __str__(self):
        return f"Данные со станции {self.station.name} в {self.date}"

    class Meta:
        verbose_name = 'Данные'
        verbose_name_plural = 'Данные'


class Street(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'street'
        verbose_name_plural = 'Улицы'
        verbose_name = 'Улица'

    def __str__(self):
        return f'{self.name}'


class AddPollution(models.Model):
    fio = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=20, blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)
    character = models.CharField(max_length=50, blank=True, null=True)
    time = models.DateTimeField(auto_now=False, blank=True, null=True)
    # name_industry = models.CharField(max_length=40, blank=True, null=True)
    name_industry = models.ForeignKey(Industry, on_delete=CASCADE, null=True, blank=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    street = models.ForeignKey(Street, on_delete=CASCADE, blank=True, null=True)
    house_number = models.CharField(max_length=8, blank=True, null=True)
    comment = models.CharField(max_length=120, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False, verbose_name='Подтверждение жалобы')

    class Meta:
        db_table = 'add_pollution'
        verbose_name_plural = 'Заявление о загрязнении'
        verbose_name = 'Заявления о загрязнениях'

    def __str__(self):
        return f'{self.email}'

    # def get_absolute_url(self):
    #     return reverse('add_pollution', kwargs={'id': self.id})

class Building(models.Model):
    id_build = models.CharField(max_length=300, blank=True, null=True, verbose_name='Ид работ')
    status = models.CharField(max_length=300, blank=True, null=True, verbose_name='Статус')
    name = models.CharField(max_length=300, blank=True, null=True, verbose_name='Название')
    func = models.CharField(max_length=300, blank=True, null=True, verbose_name='Функция')
    url = models.CharField(max_length=300, blank=True, null=True, verbose_name='Название')
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name='Адрес')
    dev = models.CharField(max_length=300, blank=True, null=True, verbose_name='Подрядчик')
    end_year = models.CharField(max_length=300, blank=True, null=True, verbose_name='Год окончания работ')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Стройка'
        verbose_name_plural = 'Стройки'




class Prediction(models.Model):
    name = models.CharField(max_length=100, verbose_name='Время')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name='Станция')
    NO = models.FloatField(verbose_name='NO', blank=True, null=True)
    NO2 = models.FloatField(verbose_name='NO2', blank=True, null=True)
    CO = models.FloatField(verbose_name='CO', blank=True, null=True)
    MP10 = models.FloatField(verbose_name='MP10', blank=True, null=True)
    MP25 = models.FloatField(verbose_name='MP2.5', blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предсказание'
        verbose_name_plural = 'Предсказания'
