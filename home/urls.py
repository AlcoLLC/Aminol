from django.urls import path
from .views import home_view, career_view, product_view

urlpatterns = [
    path("", home_view),
    path('career/', career_view, name='career'),
    path('product/', product_view, name='product'),
]