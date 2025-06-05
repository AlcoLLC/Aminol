from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Department, Job, JobApplication
import json
import logging

logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def career_view(request):
    departments = Department.objects.filter(is_active=True).order_by('name')
    jobs = Job.objects.filter(is_active=True).select_related('department').order_by('-created_at')
    
    selected_department = request.GET.get('department', 'all')
    
    if selected_department and selected_department != 'all':
        jobs = jobs.filter(department__slug=selected_department)
    
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
        'departments': departments,
        'jobs': jobs,
        'selected_department': selected_department,
        'form_labels': form_labels,
        'help_choices': help_choices,
    }
    
    return render(request, 'career.html', context)

def career_steps_view(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    if request.method == 'POST':
        return handle_job_application(request, job) 
    
    context = {
        'job': job,
        'form_labels': {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email'),
            'phone': _('Phone'),
            'cv_file': _('Upload CV file'),
            'motivation_letter': _('Your motivation letter'),
            'required': '*',
            'continue_button': _('Continue'),
            'back_button': _('Back'),
            'confirm_button': _('Confirm and send'),
            'cancel_button': _('Cancel')
        }
    }
    
    return render(request, 'career_steps.html', context)

def send_application_emails(application):
    """Job application için email gönderme fonksiyonu"""
    try:
        admin_email_subject = f"New Job Application: {application.job.title} - {application.first_name} {application.last_name}"
        admin_email_message = f"""
New Job Application Received

Job Position: {application.job.title}
Department: {application.job.department.name}
Applicant Name: {application.first_name} {application.last_name}
Email: {application.email}
Phone: {application.phone}
Applied on: {application.applied_at.strftime('%Y-%m-%d %H:%M')}

Motivation Letter:
{application.motivation_letter}

CV file has been attached to this application.
"""
        
        try:
            html_admin_email = render_to_string('emails/job_application_admin.html', {
                'application': application,
                'job': application.job,
                'applicant_name': f"{application.first_name} {application.last_name}",
                'department': application.job.department.name,
                'applied_date': application.applied_at.strftime('%Y-%m-%d %H:%M')
            })
        except:
            html_admin_email = None
        
        logger.debug(f"Email settings: HOST={settings.EMAIL_HOST}, PORT={settings.EMAIL_PORT}, USER={settings.EMAIL_HOST_USER}")
        
        admin_email_sent = send_mail(
            admin_email_subject,
            admin_email_message,
            settings.EMAIL_HOST_USER,
            ['info@aminol.az'], 
            html_message=html_admin_email,
            fail_silently=False,
        )
        
        if admin_email_sent:
            logger.info(f"Admin job application email sent successfully for application ID: {application.id}")
        else:
            logger.error(f"Failed to send admin job application email for application ID: {application.id}")
        
        user_email_subject = f"Thank you for your application - {application.job.title}"
        user_email_message = f"""
Dear {application.first_name},

Thank you for your interest in the {application.job.title} position at Aminol.

We have received your application and our HR team will review it carefully. We will contact you if your profile matches our requirements.

Job Details:
- Position: {application.job.title}
- Department: {application.job.department.name}
- Application Date: {application.applied_at.strftime('%Y-%m-%d %H:%M')}

Best regards,
Aminol HR Team
"""
        
        try:
            html_user_email = render_to_string('emails/job_application_user.html', {
                'first_name': application.first_name,
                'job_title': application.job.title,
                'department': application.job.department.name,
                'applied_date': application.applied_at.strftime('%Y-%m-%d %H:%M')
            })
        except:
            html_user_email = None
        
        user_email_sent = send_mail(
            user_email_subject,
            user_email_message,
            settings.EMAIL_HOST_USER,
            [application.email],
            html_message=html_user_email,
            fail_silently=False,
        )
        
        if user_email_sent:
            logger.info(f"User confirmation email sent successfully to {application.email} for application ID: {application.id}")
        else:
            logger.error(f"Failed to send user confirmation email to {application.email} for application ID: {application.id}")
        
        return admin_email_sent and user_email_sent
        
    except Exception as e:
        logger.error(f"Error sending application emails for application ID {application.id}: {str(e)}", exc_info=True)
        return False

def handle_job_application(request, job):
    try:
        client_ip = get_client_ip(request)

        if client_ip and JobApplication.objects.filter(job=job, ip_address=client_ip).exists():
            return JsonResponse({
                'success': False,
                'message': _('You have already applied for this job from this IP address.')
            })

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        cv_file = request.FILES.get('cv_file')
        motivation_letter = request.POST.get('motivation_letter', '').strip()
        
        if not all([first_name, last_name, email, phone, cv_file, motivation_letter]):
            return JsonResponse({
                'success': False,
                'message': _('Please fill all required fields and upload your CV.')
            })
        
        application = JobApplication.objects.create(
            job=job,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            cv_file=cv_file,
            motivation_letter=motivation_letter,
            ip_address=client_ip
        )
        
        email_sent = send_application_emails(application)
        
        if email_sent:
            logger.info(f"Job application emails sent successfully for application ID: {application.id}")
            message = _('Your application has been successfully submitted. You will receive a confirmation email shortly.')
        else:
            logger.warning(f"Job application saved but emails failed for application ID: {application.id}")
            message = _('Your application has been successfully submitted, but there was an issue sending confirmation emails.')
        
        return JsonResponse({
            'success': True,
            'message': message,
            'application_id': application.id
        })
        
    except Exception as e:
        logger.error(f"Error in handle_job_application: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': _('An error occurred while submitting your application. Please try again.')
        })

@csrf_exempt
def career_application_step(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            step = data.get('step')
            form_data = data.get('form_data', {})

            if step == 1:
                required_fields = ['first_name', 'last_name', 'email', 'phone']
            elif step == 2:
                required_fields = ['cv_file']
            elif step == 3:
                required_fields = ['motivation_letter']
            else:
                return JsonResponse({
                    'valid': False,
                    'message': _('Invalid step')
                })
            
            missing_fields = []
            for field in required_fields:
                value = form_data.get(field)
                if isinstance(value, str):
                    value = value.strip()
                if not value:
                    missing_fields.append(field)
            
            if missing_fields:
                return JsonResponse({
                    'valid': False,
                    'message': _('Please fill in all required fields: {}').format(', '.join(missing_fields))
                })
            
            return JsonResponse({'valid': True})
            
        except json.JSONDecodeError:
            return JsonResponse({
                'valid': False,
                'message': _('Invalid request format')
            })
        except Exception as e:
            logger.error(f"Error in career_application_step: {str(e)}", exc_info=True)
            return JsonResponse({
                'valid': False,
                'message': _('An error occurred while validating the form')
            })
    
    return JsonResponse({
        'valid': False,
        'message': _('Invalid request method')
    })

def filter_jobs_by_department(request):
    if request.method == 'GET':
        department_slug = request.GET.get('department', 'all')
        
        jobs_query = Job.objects.filter(is_active=True).select_related('department').order_by('-created_at')
        
        if department_slug != 'all':
            jobs_query = jobs_query.filter(department__slug=department_slug)
        
        jobs_data = []
        for job in jobs_query:
            jobs_data.append({
                'id': job.id,
                'title': job.title,
                'description': job.job_description[:100] + '...' if len(job.job_description) > 100 else job.job_description,
                'department': job.department.name,
                'work_type': job.get_work_type_display(),
                'time_type': job.get_time_type_display(),
                'apply_url': f'/career/apply/{job.id}/'
            })
        
        return JsonResponse({
            'success': True,
            'jobs': jobs_data
        })
    
    return JsonResponse({
        'success': False,
        'message': _('Invalid request')
    })