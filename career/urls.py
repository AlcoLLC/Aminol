from django.urls import path
from . import views

app_name = 'career'

urlpatterns = [
    path('career/', views.career_view, name='career'),
    path('career_steps/', views.career_steps_view, name='career_steps'),
]

