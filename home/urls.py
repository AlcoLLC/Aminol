from django.urls import path
from .views import home_view, service_aminol_dealer_view, service_laboratory_view, service_logistics_view, markets_automotive_view, markets_industrial_view, markets_shipping_view, contact_view

urlpatterns = [
    path("", home_view),
    path('service_aminol_dealer/', service_aminol_dealer_view,
         name='service_aminol_dealer'),
    path('service_laboratory/', service_laboratory_view, name='service_laboratory'),
    path('service_logistics/', service_logistics_view, name='service_logistics'),
    path('markets_automotive/', markets_automotive_view, name='markets_automotive'),
    path('markets_industrial/', markets_industrial_view, name='markets_industrial'),
    path('markets_shipping/', markets_shipping_view, name='markets_shipping'),
    path('contact/', contact_view, name='contact'),
]
