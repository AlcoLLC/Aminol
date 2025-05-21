from django.urls import path
from .views import home_view, brand_portal_view, career_view


urlpatterns = [
    path("", home_view),
    path('brand_portal/', brand_portal_view, name='brand_portal'),
    path('career/', career_view, name='career'),
]