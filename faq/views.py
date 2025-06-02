from django.shortcuts import render
from django.views.generic import ListView
from .models import FAQ

def faq_view(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('created_at')
    form_labels = {
        'help_type': _('How can we help you?'),
        'company': _('Company name'),           
        'question': _('Your question, wish and/or clarification'),
        'first_name': _('First name'),        
        'last_name': _('Last name'),           
        'email': _('Email address'),        
        'phone': _('Phone number'),             
        'required': '*',                       
        'send_button': _('Send')               
    }
    return render(request, 'faq.html', {'faqs': faqs, 'form_labels': form_labels})

class FAQListView(ListView):
    model = FAQ
    template_name = 'faq.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('created_at')