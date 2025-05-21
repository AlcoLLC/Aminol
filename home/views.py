from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')

def brand_portal_view(request):
    return render(request, 'brand_portal.html')

def faq_view(request):
    return render(request, 'faq.html')

def career_view(request):
    return render(request, 'career.html')

def news_view(request):
    return render(request, 'news.html')
