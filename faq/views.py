from django.shortcuts import render
from django.views.generic import ListView
from .models import FAQ
from django.utils.translation import gettext_lazy as _

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

    help_choices = [
        ('buy', _('I would like to buy Aminol products.')),
        ('become_dealer', _('I am interested in becoming a distributor.')),
        ('technical', _('I need technical support.')),
        ('certificates', _('I would like to request product certificates or compliance documents.')),
        ('about', _('I need more information about a product.')),
        ('partnership', _('I am interested in a potential partnership.')),
        ('other', _('Other'))
    ]

    return render(request, 'faq.html', {'faqs': faqs, 'form_labels': form_labels, 'help_choices': help_choices,})

class FAQListView(ListView):
    model = FAQ
    template_name = 'faq.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('created_at')