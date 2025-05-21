from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')

def career_view(request):
    return render(request, 'career.html')

def product_view(request):
    return render(request, 'product.html')
