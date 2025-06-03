from django.urls import path
from . import views

app_name = 'career'

urlpatterns = [
    path('career/', views.career_view, name='career'),
    path('apply/<int:job_id>/', views.career_steps_view, name='career_steps'),
    path('application-step/', views.career_application_step, name='application_step'),
    path('filter-jobs/', views.filter_jobs_by_department, name='filter_jobs'),
]