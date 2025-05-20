from django.urls import path
<<<<<<< HEAD
from .views import home_view, service_aminol_dealer_view, service_laboratory_view, service_logistics_view, markets_automotive_view, markets_industrial_view, markets_shipping_view, contact_view
=======
from .views import home_view, markets_automotive_view, markets_industrial_view, markets_shipping_view
>>>>>>> f376d9a5a1ed5d56cba2a883510474d7facae5e8

urlpatterns = [
    path("", home_view),
    path('markets_automotive/', markets_automotive_view, name='markets_automotive'),
    path('markets_industrial/', markets_industrial_view, name='markets_industrial'),
    path('markets_shipping/', markets_shipping_view, name='markets_shipping'),
    path('contact/', contact_view, name='contact'),
]
