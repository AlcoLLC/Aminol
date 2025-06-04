from django.shortcuts import render
from .models import (
    Aminol_Official_Dealer,
    Aminol_Official_Dealer_Content,
    Aminol_Labaratory,
    Aminol_Logistics
)
from news.models import News
from home.models import PartnerLogo, Gallery as GalleryImage, Supplier
from django.utils.translation import gettext_lazy as _


def aminol_dealer_view(request):
    dealer = Aminol_Official_Dealer.objects.last()
    dealer_contents = Aminol_Official_Dealer_Content.objects.filter(aminol_official_dealer=dealer) if dealer else []
    partner_logos = PartnerLogo.objects.all()
    supplier_logos = Supplier.objects.all()
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
    
    context = {
        'dealer': dealer,
        'dealer_contents': dealer_contents,
        'partner_logos': partner_logos,
        'supplier_logos': supplier_logos,
        'form_labels':form_labels,
        'help_choices': help_choices,
    }
    
    return render(request, 'service_aminol_dealer.html', context)

def aminol_laboratory_view(request):
    laboratories = Aminol_Labaratory.objects.all()
    latest_news = News.objects.filter(is_active=True)[:3]
    partner_logos = PartnerLogo.objects.all()
    supplier_logos = Supplier.objects.all()
    
    context = {
        'laboratories': laboratories,
        'latest_news': latest_news,
        'partner_logos': partner_logos,
        'supplier_logos': supplier_logos
    }
    
    return render(request, 'service_laboratory.html', context)

def aminol_logistics_view(request):
    logistics = Aminol_Logistics.objects.all()
    latest_news = News.objects.filter(is_active=True)[:3]
    partner_logos = PartnerLogo.objects.all()
    supplier_logos = Supplier.objects.all()
    
    context = {
        'logistics': logistics,
        'latest_news': latest_news,
        'partner_logos': partner_logos,
        'supplier_logos': supplier_logos
    }
    
    return render(request, 'service_logistics.html', context)