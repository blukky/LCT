from .views import *
from django.urls import path


urlpatterns = [
    path("", map, name='map'),
    path("statistics", statistics, name='statistics'),
    path("predict", predict, name='predict'),
    path("create_model", create_model, name='create_model'),
    path("docs", docs, name='docs'),
    path("location", location, name='location'),
    path("model_ajax", create_model_ajax, name='create_model_ajax'),
    path("save_model", save_model, name='save_model'),
    path("cancel_model", cancel_model, name='cancel_model'),
    path("get_pred", get_pred, name='get_pred'),

]
