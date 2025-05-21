from django.shortcuts import render, get_object_or_404
from .models import Brand_Portal, Brand_Portal_Content

def brand_portal_list(request):
    brand = Brand_Portal.objects.last()
    brand_contents = Brand_Portal_Content.objects.filter(brand_portal=brand) if brand else []
    
    context = {
        'brand': brand,
        'brand_contents': brand_contents,
    }
    
    return render(request, 'brand_portal.html', context)


def brand_portal_detail(request, pk):
    brand_portal = get_object_or_404(Brand_Portal, pk=pk)
    brand_portal_contents = Brand_Portal_Content.objects.filter(brand_portal=brand_portal)
    
    context = {
        'brand_portal': brand_portal,
        'brand_portal_contents': brand_portal_contents,
    }
    return render(request, 'brand_portal/brand_portal_detail.html', context)