from django.urls import path
from . import views

app_name = 'markets'

urlpatterns = [
    path('markets_automotive/', views.automotive, name='automotive'),
    path('markets_industrial/', views.industrial, name='industrial'),
    path('markets_shipping/', views.shipping, name='shipping'),
]