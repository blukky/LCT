from django.contrib import admin
from .models import *


# @admin.register(AddPollution)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'fio', 'telephone', 'character', 'time',
#                     'name_industry', 'city', 'comment', 'created_date', 'active')
#     list_filter = ('created_date', 'active', 'city', 'time',)
#     list_editable = ('active',)
#     search_fields = ('fio', 'email', 'telephone', 'name_industry', 'city', 'street',
#                      'house_number',)
#     autocomplete_fields = ('street', 'name_industry',)


# @admin.register(Street)
# class StreetAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'id',)
#     search_fields = ('name',)
#     ordering = ('id',)


# @admin.register(Station)
# class StationAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'lat', 'lon')
#     search_fields = ('name',)
#     ordering = ('id',)
#
#
# @admin.register(Industry)
# class IndustryAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'lat', 'lon', 'index', 'address', 'telephone', 'email')
#     search_fields = ('name', 'address', 'telephone', 'email')
#     ordering = ('-id',)

admin.site.register(Station)
admin.site.register(Industry)
admin.site.register(Data)
admin.site.register(Street)
admin.site.register(AddPollution)
admin.site.register(Building)
admin.site.register(Prediction)
admin.site.register(Rubbish)

admin.site.site_title = "MosEcoMonitoring Service"
admin.site.site_header = "MosEcoMonitoring Service"