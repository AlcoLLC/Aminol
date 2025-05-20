from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')

def service_aminol_dealer_view(request):
    return render(request, 'service_aminol_dealer.html')


def service_laboratory_view(request):
    return render(request, 'service_laboratory.html')


def service_logistics_view(request):
    return render(request, 'service_logistics.html')


def markets_automotive_view(request):
    return render(request, 'markets_automotive.html')


def markets_industrial_view(request):
    return render(request, 'markets_industrial.html')


def markets_shipping_view(request):
    return render(request, 'markets_shipping.html')
