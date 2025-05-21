from django.shortcuts import render
from .models import (
    Aminol_Official_Dealer,
    Aminol_Official_Dealer_Content,
    Aminol_Labaratory,
    Aminol_Logistics
)
from news.models import News


def aminol_dealer_view(request):
    dealer = Aminol_Official_Dealer.objects.last()
    dealer_contents = Aminol_Official_Dealer_Content.objects.filter(aminol_official_dealer=dealer) if dealer else []
    
    context = {
        'dealer': dealer,
        'dealer_contents': dealer_contents,
    }
    
    return render(request, 'service_aminol_dealer.html', context)

def aminol_laboratory_view(request):
    laboratories = Aminol_Labaratory.objects.all()
    latest_news = News.objects.filter(is_active=True)[:3]
    
    context = {
        'laboratories': laboratories,
        'latest_news': latest_news,
    }
    
    return render(request, 'service_laboratory.html', context)

def aminol_logistics_view(request):
    logistics = Aminol_Logistics.objects.all()
    latest_news = News.objects.filter(is_active=True)[:3]
    
    context = {
        'logistics': logistics,
        'latest_news': latest_news,
    }
    
    return render(request, 'service_logistics.html', context)