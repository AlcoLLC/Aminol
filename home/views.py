from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')

def brand_portal_view(request):
    return render(request, 'brand_portal.html')

def career_view(request):
    return render(request, 'career.html')
