from django.urls import path

from . import views

app_name = 'radius'
urlpatterns = [
    path('authenticate', views.authenticate, name='authenticate'),
    path('<str:action>', views.action_handler, name='action_handler'),
]
