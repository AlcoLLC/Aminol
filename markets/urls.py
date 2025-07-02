from django.urls import path
from . import views

app_name = 'markets'

urlpatterns = [
    path('markets/automotive/', views.automotive, name='automotive'),
    path('markets/industrial/', views.industrial, name='industrial'),
    path('markets/shipping/', views.shipping, name='shipping'),
]