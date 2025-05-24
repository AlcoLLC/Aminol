from django.shortcuts import render
from news.models import News
from products.models import Product_group


def home_view(request):
    latest_news = News.objects.filter(is_active=True)[:3]
    product_groups = Product_group.objects.all()
    context = {
        'latest_news': latest_news,
        'product_groups':product_groups
    }
    
    return render(request, 'home.html', context)

def career_view(request):
    return render(request, 'career.html')

