from django.contrib import admin
from .models import Contact, ContactInfo, ContactSubmissionLimit
from modeltranslation.admin import TranslationAdmin

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company_name', 'help_type', 'email', 'ip_address', 'created_at']
    list_filter = ['help_type', 'created_at', 'ip_address']
    search_fields = ['first_name', 'last_name', 'company_name', 'email', 'ip_address']
    readonly_fields = ['ip_address', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'company_name', 'email', 'phone_number')
        }),
        ('Inquiry Details', {
            'fields': ('help_type', 'question')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'created_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ContactSubmissionLimit)
class ContactSubmissionLimitAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'submission_count', 'last_submission', 'is_blocked', 'created_at']
    list_filter = ['is_blocked', 'last_submission', 'created_at']
    search_fields = ['ip_address']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-last_submission']
    
    actions = ['unblock_ips', 'reset_submission_count']
    
    def unblock_ips(self, request, queryset):
        updated = queryset.update(is_blocked=False)
        self.message_user(request, f'{updated} IP addresses have been unblocked.')
    unblock_ips.short_description = 'Unblock selected IP addresses'
    
    def reset_submission_count(self, request, queryset):
        updated = queryset.update(submission_count=0)
        self.message_user(request, f'Submission count reset for {updated} IP addresses.')
    reset_submission_count.short_description = 'Reset submission count for selected IPs'



@admin.register(ContactInfo)
class ContactInfoAdmin(TranslationAdmin):
    list_display = ('title', 'contact_email', 'contact_phone')
    search_fields = ('title', 'description', 'contact_email')
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'description', 'title_translate', 'description_translate')
        }),
        ('Headquarters Information', {
            'fields': ('aminol_headquarters', 'aminol_headquarters_location', 'aminol_headquarters_image',
                        'aminol_headquarters_translate', 'aminol_factory_translate')
        }),
        ('Factory Information', {
            'fields': ('aminol_factory', 'aminol_factory_location', 'aminol_factory_image')
        }),
        ('Registration Information', {
            'fields': ('registers','registers_translate')
        }),
        ('Contact Details', {
            'fields': ('contact_address', 'contact_address_translate', 'contact_phone', 'contact_email')
        }),
    )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }