from django.shortcuts import render, get_object_or_404
from .models import News

def news_list(request):
    all_news = News.objects.filter(is_active=True)
    latest_news = News.objects.filter(is_active=True)[:3]
    
    context = {
        'all_news': all_news,
        'latest_news': latest_news,
    }
    
    return render(request, 'news.html', context)

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk, is_active=True)
    
    latest_news = News.objects.filter(is_active=True)[:3]
    
    context = {
        'news': news,
        'latest_news': latest_news,
    }
    return render(request, 'news_detail.html', context)
