from django.contrib import admin
from .models import Brand_Portal, Brand_Portal_Content

class Brand_Portal_ContentInline(admin.TabularInline):
    model = Brand_Portal_Content
    extra = 1

@admin.register(Brand_Portal)
class Brand_PortalAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    inlines = [Brand_Portal_ContentInline]

@admin.register(Brand_Portal_Content)
class Brand_Portal_ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand_portal', 'created_at', 'updated_at')
    list_filter = ('brand_portal', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')