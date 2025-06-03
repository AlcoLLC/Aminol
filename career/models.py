from django.db import models
from django.utils.translation import gettext_lazy as _

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Department Name'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name']

    def __str__(self):
        return self.name

class Job(models.Model):
    WORK_TYPE_CHOICES = [
        ('remote', _('100% Remote')),
        ('on_site', _('100% On-site')),
        ('hybrid', _('Hybrid')),
    ]
    
    TIME_TYPE_CHOICES = [
        ('full_time', _('Full-time')),
        ('part_time', _('Part-time')),
    ]

    title = models.CharField(max_length=200, verbose_name=_('Job Title'))
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name=_('Department'))
    job_description = models.TextField(verbose_name=_('Job Description'))
    requirements = models.TextField(verbose_name=_('Requirements'))
    responsibilities = models.TextField(verbose_name=_('Responsibilities'))
    bonus_skills = models.TextField(blank=True, verbose_name=_('Bonus Skills'))
    
    work_type = models.CharField(
        max_length=20,
        choices=WORK_TYPE_CHOICES,
        verbose_name=_('Work Type')
    )
    
    time_type = models.CharField(
        max_length=20,
        choices=TIME_TYPE_CHOICES,
        verbose_name=_('Time Type')
    )
    
    
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.department.name}"

class JobApplication(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('reviewing', _('Under Review')),
        ('interview', _('Interview Stage')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name=_('Job'))
    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
    cv_file = models.FileField(upload_to='cv_files/', verbose_name=_('CV File'))
    motivation_letter = models.TextField(verbose_name=_('Motivation Letter'))
    
    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Job Application')
        verbose_name_plural = _('Job Applications')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.title}"