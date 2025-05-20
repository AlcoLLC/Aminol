from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')

def markets_automotive_view(request):
    return render(request, 'markets_automotive.html')


def markets_industrial_view(request):
    return render(request, 'markets_industrial.html')


def markets_shipping_view(request):
    return render(request, 'markets_shipping.html')

def contact_view(request):
    return render(request, 'contact.html')
