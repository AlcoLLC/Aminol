from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import Department, Job, JobApplication
import json

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
    
    context = {
        'departments': departments,
        'jobs': jobs,
        'selected_department': selected_department,
        'form_labels': form_labels 
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

def handle_job_application(request, job):
    try:
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        cv_file = request.FILES.get('cv_file')
        motivation_letter = request.POST.get('motivation_letter', '').strip()
        
        if not all([first_name, last_name, email, phone, cv_file, motivation_letter]):
            return JsonResponse({
                'success': False,
                'message': _('Please fill all required fields.')
            })
        
        application = JobApplication.objects.create(
            job=job,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            cv_file=cv_file,
            motivation_letter=motivation_letter
        )
        
        return JsonResponse({
            'success': True,
            'message': _('Your application has been successfully submitted.'),
            'application_id': application.id
        })
        
    except Exception as e:
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
                if not form_data.get(field):
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
        
        jobs = Job.objects.filter(is_active=True).select_related('department')
        
        if department_slug != 'all':
            jobs = jobs.filter(department__slug=department_slug)
        
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                'id': job.id,
                'title': job.title,
                'description': job.job_description[:100] + '...' if len(job.job_description) > 100 else job.job_description,
                'department': job.department.name,
                'work_type': job.get_work_type_display(),
                'time_type': job.get_time_type_display(),
                'apply_url': f'/apply/{job.id}/'
            })
        
        return JsonResponse({
            'success': True,
            'jobs': jobs_data
        })
    
    return JsonResponse({
        'success': False,
        'message': _('Invalid request')
    })