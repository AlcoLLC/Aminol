from django.urls import path
from . import views

urlpatterns = [
    path('service_aminol_dealer/', views.aminol_dealer_view, name='aminol_dealer'),
    path('service_laboratory/', views.aminol_laboratory_view, name='aminol_laboratory'),
    path('service_logistics/', views.aminol_logistics_view, name='aminol_logistics'),
]

