from django.urls import path
from .views import about_view, home_view

urlpatterns = [
    path("", home_view),
    path('about/', about_view, name='about'),
]
