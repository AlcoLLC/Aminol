from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from .models import Contact, ContactInfo
from .forms import ContactForm
import logging
import requests
from django.utils.translation import gettext_lazy as _

# Ensure you have RECAPTCHA keys in your settings
RECAPTCHA_SITE_KEY = settings.RECAPTCHA_SITE_KEY
RECAPTCHA_SECRET_KEY = settings.RECAPTCHA_SECRET_KEY

logger = logging.getLogger(__name__)

def verify_recaptcha(recaptcha_response):
    """
    Verify reCAPTCHA response with Google's API
    """
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    
    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()
        
        logger.debug(f"reCAPTCHA verification result: {result}")
        
        return result.get('success', False)
    except Exception as e:
        logger.error(f"reCAPTCHA verification error: {str(e)}")
        return False

def contact_view(request):
    help_choices = [
        ('buy', _('I would like to buy Aminol products.')),
        ('become_dealer', _('I am interested in becoming a distributor.')),
        ('technical', _('I need technical support.')),
        ('other', _('Other'))
    ]

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
    
    if request.method == 'POST':
        # Verify reCAPTCHA first
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        if not recaptcha_response:
            messages.error(request, _("Please complete the reCAPTCHA verification."))
            logger.warning("Form submission without reCAPTCHA response")
        elif not verify_recaptcha(recaptcha_response):
            messages.error(request, _("reCAPTCHA verification failed. Please try again."))
            logger.warning(f"reCAPTCHA verification failed for response: {recaptcha_response}")
        else:
            # Process form if reCAPTCHA is valid
            form_data = {
                'help_type': request.POST.get('helpType'),
                'company_name': request.POST.get('company'),
                'question': request.POST.get('question'),
                'first_name': request.POST.get('firstName'),
                'last_name': request.POST.get('lastName'),
                'email': request.POST.get('email'),
                'phone_number': request.POST.get('phone'),
            }
            
            form = ContactForm(form_data)
            
            if form.is_valid():
                try:
                    form.save()
                    
                    help_type_display = dict(Contact.HELP_CHOICES).get(form.cleaned_data['help_type'])
                    
                    email_subject = f"New Contact Form Submission from {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
                    email_message = f"""
Name: {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}
Company: {form.cleaned_data['company_name']}
Email: {form.cleaned_data['email']}
Phone: {form.cleaned_data['phone_number']}
Help Type: {help_type_display}
Question/Message: {form.cleaned_data['question']}

Note: This submission was verified with reCAPTCHA.
"""
                    html_email = render_to_string('emails/contactform.html', {
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'company': form.cleaned_data['company_name'],
                        'email': form.cleaned_data['email'],
                        'phone_number': form.cleaned_data['phone_number'],
                        'help_type': help_type_display,
                        'message': form.cleaned_data['question']
                    })
                    
                    logger.debug(f"Email settings: HOST={settings.EMAIL_HOST}, PORT={settings.EMAIL_PORT}, USER={settings.EMAIL_HOST_USER}")
                    
                    send_mail(
                        email_subject,
                        email_message,
                        settings.EMAIL_HOST_USER,
                        ['info@aminol.az'],
                        html_message=html_email,
                        fail_silently=False,
                    )
                    
                    user_email_subject = "Thank you for contacting Aminol"
                    user_email_message = f"""
Dear {form.cleaned_data['first_name']},

Thank you for contacting Aminol. We have received your inquiry. Our team will get back to you shortly.

Best regards,
Aminol Support Team
"""
                    send_mail(
                        user_email_subject,
                        user_email_message,
                        settings.EMAIL_HOST_USER,
                        [form.cleaned_data['email']],
                        fail_silently=False,
                    )
                    
                    messages.success(request, _("Your message has been sent successfully. Thank you for contacting us!"))
                    return redirect('/')
                
                except Exception as e:
                    logger.error(f"Error processing form: {str(e)}", exc_info=True)
                    messages.error(request, _("An error occurred while sending your message. Please try again or contact us directly."))
                    form.add_error(None, _("An error occurred. Please try again."))

            else:
                logger.warning(f"Form validation errors: {form.errors}")
                messages.error(request, _("Please correct the errors in the form."))

    contact_info = ContactInfo.objects.last()
    
    context = {
        'help_choices': help_choices,
        'contact_info': contact_info,
        'form_labels': form_labels,
        'recaptcha_site_key': RECAPTCHA_SITE_KEY
    }
    
    return render(request, 'contact.html', context)