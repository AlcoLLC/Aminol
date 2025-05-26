from django.shortcuts import render
from news.models import News
from products.models import Product_group
from .models import BrandLogo, CarLogos

def home_view(request): 
    latest_news = News.objects.filter(is_active=True)[:3] 
    product_groups = Product_group.objects.all()
    brand_logos = BrandLogo.objects.all()
    car_logos = CarLogos.objects.all()
    
    context = { 
        'latest_news': latest_news, 
        'product_groups': product_groups,
        'brand_logos': brand_logos,
        'car_logos': car_logos,
    } 
     
    return render(request, 'home.html', context)