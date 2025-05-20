from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages 
from django.conf import settings
from .models import Contact
from .forms import ContactForm
import logging  

logger = logging.getLogger(__name__)

def contact_view(request):
    help_choices = Contact.HELP_CHOICES
    
    if request.method == 'POST':
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
                contact = form.save()
                
                help_type_display = dict(Contact.HELP_CHOICES).get(form.cleaned_data['help_type'])
                
                email_subject = f"New Contact Form Submission from {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
                email_message = f"""
Name: {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}
Company: {form.cleaned_data['company_name']}
Email: {form.cleaned_data['email']}
Phone: {form.cleaned_data['phone_number']}
Help Type: {help_type_display}
Question/Message: {form.cleaned_data['question']}
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
                
                admin_email_sent = send_mail(
                    email_subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    ['aytacmehdizade08@gmail.com'], 
                    html_message=html_email,
                    fail_silently=False,
                )
                
                if admin_email_sent:
                    logger.info(f"Admin email sent successfully to aytacmehdizade08@gmail.com")
                else:
                    logger.error("Failed to send admin email")
                
                user_email_subject = "Thank you for contacting Aminol"
                user_email_message = f"""
Dear {form.cleaned_data['first_name']},

Thank you for contacting Aminol. We have received your inquiry. Our team will get back to you shortly.

Best regards,
Aminol Support Team
"""
                
                user_email_sent = send_mail(
                    user_email_subject,
                    user_email_message,
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email']], 
                    fail_silently=False,
                )
                
                if user_email_sent:
                    logger.info(f"User confirmation email sent successfully to {form.cleaned_data['email']}")
                else:
                    logger.error(f"Failed to send user confirmation email to {form.cleaned_data['email']}")
                
                messages.success(request, "Your message has been sent successfully. Thank you for contacting us!")
                return redirect('/')
            
            except Exception as e:
                logger.error(f"Error processing form: {str(e)}", exc_info=True)
                messages.error(request, "An error occurred while sending your message. Please try again or contact us directly.")
                form.add_error(None, "An error occurred. Please try again.")

        else:
            logger.warning(f"Form validation errors: {form.errors}")
            messages.error(request, "Please correct the errors in the form.")
    
    context = {
        'help_choices': help_choices,
    }
    
    print("Context help_choices:", context['help_choices'])

    return render(request, 'service_aminol_dealer.html', context)