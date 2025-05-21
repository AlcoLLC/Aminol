from django.shortcuts import render
from django.views.generic import ListView
from .models import FAQ

def faq_view(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('created_at')
    return render(request, 'faq.html', {'faqs': faqs})

class FAQListView(ListView):
    model = FAQ
    template_name = 'faq.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('created_at')