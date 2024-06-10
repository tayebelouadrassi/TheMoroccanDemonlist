from django.urls import path
from . import views

app_name = 'level'

urlpatterns = [
    path('<int:pk>/', views.detail, name='classic_level_detail'),
    path('classic-mainlist/', views.classic_mainlist, name='classic_mainlist'),
    path('classic-extendedlist/', views.classic_extendedlist, name='classic_extendedlist'),
    path('classic-legacylist/', views.classic_legacylist, name='classic_legacylist'),
    path('classic-stat-viewer/', views.classic_stat_viewer, name='classic_statviewer'),
    path('platformer-mainlist/', views.platformer_mainlist, name='platformer_mainlist'),
    path('platformer-stat-viewer/', views.platformer_stat_viewer, name='platformer_statviewer'),
    path('search/', views.search, name='search'),
]