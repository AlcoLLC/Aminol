from django.shortcuts import render
from news.models import News


def home_view(request):
    latest_news = News.objects.filter(is_active=True)[:3]
    context = {
        'latest_news': latest_news,
    }
    
    return render(request, 'home.html', context)

def career_view(request):
    return render(request, 'career.html')

