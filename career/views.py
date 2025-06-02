from django.shortcuts import render
from django.views.generic import ListView
# from .models import Career

def career_view(request):
    return render(request, 'career.html')

def career_steps_view(request):
    return render(request, 'career_steps.html')
