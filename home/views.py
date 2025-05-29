from django.shortcuts import render
from news.models import News
from products.models import Product_group
from .models import PartnerLogo, Gallery as GalleryImage, Supplier

def home_view(request): 
    latest_news = News.objects.filter(is_active=True)[:3] 
    
    product_groups = Product_group.objects.all().order_by('-in_home', 'order')
    
    partner_logos = PartnerLogo.objects.all()
    supplier_logos = Supplier.objects.all()

    images = GalleryImage.objects.all().order_by('order')

    
    context = { 
        'latest_news': latest_news, 
        'product_groups': product_groups,
        'partner_logos': partner_logos,
        'supplier_logos': supplier_logos,
        'images': images,
    } 
     
    return render(request, 'home.html', context)