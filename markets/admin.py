from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import (
    Markets_Automotive, Markets_Automotive_Content,
    Markets_Industrial, Markets_Industrial_Content, Industries_Content,
    Markets_Shipping, Markets_Shipping_Content
)

class Markets_Automotive_ContentInline(TranslationTabularInline):
    model = Markets_Automotive_Content
    extra = 1

@admin.register(Markets_Automotive)
class Markets_AutomotiveAdmin(TranslationAdmin):
    inlines = [Markets_Automotive_ContentInline]
    list_display = ('title',)
    search_fields = ('title',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class Markets_Industrial_ContentInline(TranslationTabularInline):
    model = Markets_Industrial_Content
    extra = 1

class Industries_ContentInline(TranslationTabularInline):
    model = Industries_Content
    extra = 1

@admin.register(Markets_Industrial)
class Markets_IndustrialAdmin(TranslationAdmin):
    inlines = [Markets_Industrial_ContentInline, Industries_ContentInline]
    list_display = ('title',)
    search_fields = ('title',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class Markets_Shipping_ContentInline(TranslationTabularInline):
    model = Markets_Shipping_Content
    extra = 1

@admin.register(Markets_Shipping)
class Markets_ShippingAdmin(TranslationAdmin):
    inlines = [Markets_Shipping_ContentInline]
    list_display = ('title',)
    search_fields = ('title',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }