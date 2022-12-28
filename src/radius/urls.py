from django.urls import path

from . import views

app_name = 'radius'
urlpatterns = [
    path('<str:action>', views.action_handler, name='action_handler'),
]
