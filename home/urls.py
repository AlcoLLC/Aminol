from django.urls import path
from .views import home_view, markets_automotive_view, markets_industrial_view, markets_shipping_view

urlpatterns = [
    path("", home_view),
    path('markets_automotive/', markets_automotive_view, name='markets_automotive'),
    path('markets_industrial/', markets_industrial_view, name='markets_industrial'),
    path('markets_shipping/', markets_shipping_view, name='markets_shipping'),
]
