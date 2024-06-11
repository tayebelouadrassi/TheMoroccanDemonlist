from django.urls import path
from . import views

app_name = 'recordsubmission'

urlpatterns = [
    path('<str:record_type>/', views.submit_record, name='submit_record'),
]