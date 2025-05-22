from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('product/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]