# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Department, Job, JobApplication

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'job_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    def job_count(self, obj):
        return obj.job_set.count()
    job_count.short_description = _('Jobs Count')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'department', 
        'work_type', 
        'time_type', 
        'is_active',
        'application_count',
        'created_at'
    ]
    list_filter = [
        'department', 
        'work_type', 
        'time_type', 
        'is_active', 
        'created_at'
    ]
    search_fields = ['title', 'job_description', 'requirements']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'department')
        }),
        (_('Job Details'), {
            'fields': ('job_description', 'requirements', 'responsibilities', 'bonus_skills')
        }),
        (_('Work Configuration'), {
            'fields': ('work_type', 'time_type', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def application_count(self, obj):
        count = obj.jobapplication_set.count()
        if count > 0:
            return format_html(
                '<a href="/admin/your_app/jobapplication/?job__id__exact={}">{}</a>',
                obj.id, count
            )
        return count
    application_count.short_description = _('Applications')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'get_full_name',
        'job',
        'email',
        'phone',
        'status',
        'applied_at',
        'cv_link'
    ]
    list_filter = [
        'status',
        'job__department',
        'job',
        'applied_at'
    ]
    search_fields = [
        'first_name',
        'last_name', 
        'email',
        'job__title'
    ]
    list_editable = ['status']
    readonly_fields = ['applied_at', 'updated_at']
    
    fieldsets = (
        (_('Applicant Information'), {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        (_('Job Information'), {
            'fields': ('job', 'status')
        }),
        (_('Application Details'), {
            'fields': ('cv_file', 'motivation_letter')
        }),
        (_('Timestamps'), {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = _('Full Name')
    get_full_name.admin_order_field = 'first_name'
    
    def cv_link(self, obj):
        if obj.cv_file:
            return format_html(
                '<a href="{}" target="_blank">📄 {}</a>',
                obj.cv_file.url,
                _('Download CV')
            )
        return '-'
    cv_link.short_description = _('CV File')
    
    # Bulk actions
    actions = ['mark_as_reviewing', 'mark_as_interview', 'mark_as_accepted', 'mark_as_rejected']
    
    def mark_as_reviewing(self, request, queryset):
        updated = queryset.update(status='reviewing')
        self.message_user(request, f'{updated} applications marked as under review.')
    mark_as_reviewing.short_description = _('Mark as under review')
    
    def mark_as_interview(self, request, queryset):
        updated = queryset.update(status='interview')
        self.message_user(request, f'{updated} applications marked for interview.')
    mark_as_interview.short_description = _('Mark for interview')
    
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f'{updated} applications accepted.')
    mark_as_accepted.short_description = _('Mark as accepted')
    
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} applications rejected.')
    mark_as_rejected.short_description = _('Mark as rejected')