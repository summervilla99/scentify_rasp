from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.app, name='app'),
    path('app/timer/', views.timer, name='timer'),
]
