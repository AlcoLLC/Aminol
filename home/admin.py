from django.contrib import admin
from django.utils.html import format_html
from .models import BrandLogo, CarLogos


@admin.register(BrandLogo)
class BrandLogoAdmin(admin.ModelAdmin):
    list_display = ['id', 'logo_preview', 'logo_name', 'created_at', 'updated_at']
    list_display_links = ['id', 'logo_preview', 'logo_name']
    readonly_fields = ['logo_preview_large', 'created_at', 'updated_at']
    list_per_page = 20
    ordering = ['-created_at']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: contain; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.logo.url
            )
        return "No Image"
    logo_preview.short_description = "Preview"
    
    def logo_preview_large(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain; border-radius: 8px; border: 1px solid #ddd;" />',
                obj.logo.url
            )
        return "No Image"
    logo_preview_large.short_description = "Logo Preview"
    
    def logo_name(self, obj):
        if obj.logo:
            return obj.logo.name.split('/')[-1] 
        return "No File"
    logo_name.short_description = "File Name"
    
    fieldsets = (
        ('Logo Information', {
            'fields': ('logo', 'logo_preview_large')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CarLogos)
class CarLogosAdmin(admin.ModelAdmin):
    list_display = ['id', 'logo_preview', 'logo_name', 'created_at', 'updated_at']
    list_display_links = ['id', 'logo_preview', 'logo_name']
    readonly_fields = ['logo_preview_large', 'created_at', 'updated_at']
    list_per_page = 20
    ordering = ['-created_at']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: contain; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.logo.url
            )
        return "No Image"
    logo_preview.short_description = "Preview"
    
    def logo_preview_large(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain; border-radius: 8px; border: 1px solid #ddd;" />',
                obj.logo.url
            )
        return "No Image"
    logo_preview_large.short_description = "Logo Preview"
    
    def logo_name(self, obj):
        if obj.logo:
            return obj.logo.name.split('/')[-1] 
        return "No File"
    logo_name.short_description = "File Name"
    
    fieldsets = (
        ('Logo Information', {
            'fields': ('logo', 'logo_preview_large')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )