from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('services/dealer/', views.aminol_dealer_view, name='dealer'),
    path('services/laboratory/', views.aminol_laboratory_view, name='laboratory'),
    path('services/logistics/', views.aminol_logistics_view, name='logistics'),

]

