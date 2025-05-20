from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'email',
                   'phone_number', 'help_type', 'created_at')
    list_filter = ('help_type', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company_name', 'phone_number')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Company Information', {
            'fields': ('company_name',)
        }),
        ('Inquiry Details', {
            'fields': ('help_type', 'question')
        }),
        ('Additional Information', {
            'fields': ('created_at',)
        }),
    )