from django.contrib import admin
from .models import Contact, ContactInfo


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

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ContactInfo model with location fields.
    """
    list_display = ('title', 'contact_email', 'contact_phone')
    search_fields = ('title', 'description', 'contact_email')
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'description')
        }),
        ('Headquarters Information', {
            'fields': ('aminol_headquarters', 'aminol_headquarters_location', 'aminol_headquarters_image')
        }),
        ('Factory Information', {
            'fields': ('aminol_factory', 'aminol_factory_location', 'aminol_factory_image')
        }),
        ('Registration Information', {
            'fields': ('registers',)
        }),
        ('Contact Details', {
            'fields': ('contact_address', 'contact_phone', 'contact_email')
        }),
    )