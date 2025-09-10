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
    exclude=('title', 'description')

@admin.register(Aminol_Official_Dealer)
class Aminol_Official_DealerAdmin(TranslationAdmin):
    list_display = ('title_translate', 'title_description_translate')
    search_fields = ('title_translate',)
    inlines = [Aminol_Official_Dealer_ContentInline]
    exclude=('title', 'description', 'title_description')
    
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
    list_display = ('title_translate',)
    search_fields = ('title_translate',)
    exclude=('title', 'description')
    
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
    list_display = ('title_translate',)
    search_fields = ('title_translate',)
    exclude=('title', 'description')
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }