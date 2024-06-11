from django.urls import path
from . import views

app_name = 'recordsubmission'

urlpatterns = [
    path('submit-record/<str:record_type>/', views.submit_record, name='submit_record'),
    path('submissions/', views.submissions, name='submissions'),
]