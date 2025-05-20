from django.shortcuts import render
from .models import (
    Markets_Automotive, Markets_Automotive_Content,
    Markets_Industrial, Markets_Industrial_Content, Industries_Content,
    Markets_Shipping, Markets_Shipping_Content
)


def automotive(request):
    automotive_service = Markets_Automotive.objects.last()
    automotive_contents = None
    
    if automotive_service:
        automotive_contents = Markets_Automotive_Content.objects.filter(
            markets_automotive=automotive_service
        )
    
    context = {
        'automotive_service': automotive_service,
        'automotive_contents': automotive_contents,
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
    
    context = {
        'industrial_service': industrial_service,
        'industrial_contents': industrial_contents,
        'industries': industries,
        'automotive_service': automotive_service,
    }
    return render(request, 'markets_industrial.html', context)

def shipping(request):
    shipping_service = Markets_Shipping.objects.first()
    automotive_service = Markets_Automotive.objects.last() 
    shipping_contents = None
    
    if shipping_service:
        shipping_contents = Markets_Shipping_Content.objects.filter(
            markets_shipping=shipping_service 
        )
    
    context = {
        'shipping_service': shipping_service,
        'shipping_contents': shipping_contents,
        'automotive_service': automotive_service,
    }
    return render(request, 'markets_shipping.html', context)