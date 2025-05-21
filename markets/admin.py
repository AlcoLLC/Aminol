from django.contrib import admin
from .models import (
    Markets_Automotive, Markets_Automotive_Content,
    Markets_Industrial, Markets_Industrial_Content, Industries_Content,
    Markets_Shipping, Markets_Shipping_Content
)

class Markets_Automotive_ContentInline(admin.TabularInline):
    model = Markets_Automotive_Content
    extra = 1

@admin.register(Markets_Automotive)
class Markets_AutomotiveAdmin(admin.ModelAdmin):
    inlines = [Markets_Automotive_ContentInline]
    list_display = ('title',)
    search_fields = ('title',)

class Markets_Industrial_ContentInline(admin.TabularInline):
    model = Markets_Industrial_Content
    extra = 1

class Industries_ContentInline(admin.TabularInline):
    model = Industries_Content
    extra = 1

@admin.register(Markets_Industrial)
class Markets_IndustrialAdmin(admin.ModelAdmin):
    inlines = [Markets_Industrial_ContentInline, Industries_ContentInline]
    list_display = ('title',)
    search_fields = ('title',)

class Markets_Shipping_ContentInline(admin.TabularInline):
    model = Markets_Shipping_Content
    extra = 1

@admin.register(Markets_Shipping)
class Markets_ShippingAdmin(admin.ModelAdmin):
    inlines = [Markets_Shipping_ContentInline]
    list_display = ('title',)
    search_fields = ('title',)