from django.urls import path
from . import views

app_name = 'Level'

urlpatterns = [
    path('classic_mainlist', views.classic_mainlist, name='classic_mainlist'),
]