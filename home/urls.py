from django.urls import path
from .views import home_view

app_name = "home"
urlpatterns = [
    path("", home_view, name="home"),
    # path('career/', career_view, name='career'),
]