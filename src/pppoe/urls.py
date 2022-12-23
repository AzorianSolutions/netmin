from django.urls import path

from . import views

app_name = 'pppoe'
urlpatterns = [
    path('', views.index, name='index'),
]
