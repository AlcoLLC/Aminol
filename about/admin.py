from .models import (
    AboutAminol, AboutSectionContent, Quality, QualityContent,
    WeGuarantee, Production, ProductionContent,
    DocumentsCertification, Sustainability, SustainabilityContent
)

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

class AboutSectionContentInline(TranslationTabularInline):
    model = AboutSectionContent
    extra = 1
    fields = ('image', 'title_translate', 'description_translate')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(AboutAminol)
class AboutAminolAdmin(TranslationAdmin):
    inlines = [AboutSectionContentInline]
    fields = (
        'founded_year', 'workforce', 'shared_image',
        'based_in_translate', 'location_translate', 'exporting_to_translate', 'production_capacity_translate'
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


# Quality Section Admin
class QualityContentInline(TranslationTabularInline):
    model = QualityContent
    extra = 1
    fields = ('image', 'title_translate', 'description_translate')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Quality)
class QualityAdmin(admin.ModelAdmin):
    inlines = [QualityContentInline]


@admin.register(WeGuarantee)
class WeGuaranteeAdmin(TranslationAdmin):
    fields = (
        'title_translate', 'sub_title_one_translate', 'sub_description_one_translate',
        'sub_title_two_translate', 'sub_description_two_translate',
        'sub_title_three_translate', 'sub_description_three_translate',
        'sub_title_four_translate', 'sub_description_four_translate'
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


# Production Section Admin
class ProductionContentInline(TranslationTabularInline):
    model = ProductionContent
    extra = 1
    fields = ('image', 'title_translate', 'description_translate')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    inlines = [ProductionContentInline]


@admin.register(DocumentsCertification)
class DocumentsCertificationAdmin(TranslationAdmin):
    fields = ('title_translate', 'description_translate')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


# Sustainability Section Admin
class SustainabilityContentInline(TranslationTabularInline):
    model = SustainabilityContent
    extra = 1
    fields = ('image', 'title_translate', 'description_translate')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Sustainability)
class SustainabilityAdmin(TranslationAdmin):
    inlines = [SustainabilityContentInline]
    fields = ('main_description_translate',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
