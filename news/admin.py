# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'is_active', 'image_preview']
    list_filter = ['is_active', 'published_date']
    search_fields = ['title', 'content']
    list_editable = ['is_active']
    readonly_fields = ['published_date', 'image_preview']
    
    fieldsets = (
        ('News Information', {
            'fields': ('title', 'content', 'is_active')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
        ('Meta Information', {
            'fields': ('published_date',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 60px; object-fit: cover;"/>',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"
    
    class Media:
        css = {
            'all': ('admin/css/news_admin.css',)
        }