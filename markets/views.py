from django.shortcuts import render
from .models import (
    Markets_Automotive, Markets_Automotive_Content,
    Markets_Industrial, Markets_Industrial_Content, Industries_Content,
    Markets_Shipping, Markets_Shipping_Content, Market_Shipping_Logos
)
from home.models import PartnerLogo, Gallery as GalleryImage, MarketLogo, Supplier


def automotive(request):
    automotive_service = Markets_Automotive.objects.last()
    automotive_contents = None
    
    if automotive_service:
        automotive_contents = Markets_Automotive_Content.objects.filter(
            markets_automotive=automotive_service
        )

    partner_logos = PartnerLogo.objects.all()
    supplier_logos = Supplier.objects.all()
    images = GalleryImage.objects.all().order_by('order')
    
    context = {
        'automotive_service': automotive_service,
        'automotive_contents': automotive_contents,
        'partner_logos': partner_logos,
        'images': images,
        'supplier_logos': supplier_logos,
    }
    return render(request, 'markets_automotive.html', context)

def industrial(request):
    industrial_service = Markets_Industrial.objects.last()
    automotive_service = Markets_Automotive.objects.last()
    industrial_contents = None
    industries = None
    
    if industrial_service:
        industrial_contents = Markets_Industrial_Content.objects.filter(
            markets_industrial=industrial_service
        )
        industries = Industries_Content.objects.filter(
            markets_industrial=industrial_service
        )

    images = GalleryImage.objects.all().order_by('order')
    market_logos = MarketLogo.objects.all()
    partner_logos = PartnerLogo.objects.all()
    supplier_logos = Supplier.objects.all()
    
    context = {
        'industrial_service': industrial_service,
        'industrial_contents': industrial_contents,
        'industries': industries,
        'automotive_service': automotive_service,
        'images': images,
        'market_logos': market_logos,
        'partner_logos': partner_logos,
        'supplier_logos': supplier_logos,
    }
    return render(request, 'markets_industrial.html', context)

def shipping(request):
    shipping_service = Markets_Shipping.objects.first()
    automotive_service = Markets_Automotive.objects.last() 
    shipping_contents = None

    images = GalleryImage.objects.all().order_by('order')
    market_logos = MarketLogo.objects.all()
    partner_logos = PartnerLogo.objects.all()
    market_shipping_logos = Market_Shipping_Logos.objects.all().order_by('order')
    
    if shipping_service:
        shipping_contents = Markets_Shipping_Content.objects.filter(
            markets_shipping=shipping_service 
        )
    supplier_logos = Supplier.objects.all()
    context = {
        'shipping_service': shipping_service,
        'shipping_contents': shipping_contents,
        'automotive_service': automotive_service,
        'images': images,
        'market_logos': market_logos,
        'partner_logos': partner_logos,
        'supplier_logos': supplier_logos,
        'market_shipping_logos': market_shipping_logos,
    }
    return render(request, 'markets_shipping.html', context)