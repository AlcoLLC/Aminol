from django.shortcuts import render
from .models import News

def news_list(request):
    all_news = News.objects.filter(is_active=True)
    latest_news = News.objects.filter(is_active=True)[:3]
    
    context = {
        'all_news': all_news,
        'latest_news': latest_news,
    }
    
    return render(request, 'news.html', context)