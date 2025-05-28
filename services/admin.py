from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import (
    Aminol_Official_Dealer,
    Aminol_Official_Dealer_Content,
    Aminol_Labaratory,
    Aminol_Logistics
)

class Aminol_Official_Dealer_ContentInline(TranslationTabularInline):
    model = Aminol_Official_Dealer_Content
    extra = 1

@admin.register(Aminol_Official_Dealer)
class Aminol_Official_DealerAdmin(TranslationAdmin):
    list_display = ('title', 'title_description')
    search_fields = ('title',)
    inlines = [Aminol_Official_Dealer_ContentInline]
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Aminol_Labaratory)
class Aminol_LabaratoryAdmin(TranslationAdmin):
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

@admin.register(Aminol_Logistics)
class Aminol_LogisticsAdmin(TranslationAdmin):
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