from django.contrib import admin
from .models import (
    AboutAminol, AboutSectionContent, Quality, QualityContent,
    WeGuarantee, Production, ProductionContent,
    DocumentsCertification, Sustainability, SustainabilityContent
)


class AboutSectionContentInline(admin.TabularInline):
    model = AboutSectionContent
    extra = 1
    fields = ('title', 'description', 'image')


@admin.register(AboutAminol)
class AboutAminolAdmin(admin.ModelAdmin):
    inlines = [AboutSectionContentInline]
    fields = (
        'founded_year', 'based_in', 'location',
        'exporting_to', 'production_capacity', 'workforce', 'shared_image'
    )


class QualityContentInline(admin.TabularInline):
    model = QualityContent
    extra = 1
    fields = ('title', 'description', 'image')


@admin.register(Quality)
class QualityAdmin(admin.ModelAdmin):
    inlines = [QualityContentInline]


@admin.register(WeGuarantee)
class WeGuaranteeAdmin(admin.ModelAdmin):
    fields = (
        'title',
        'sub_title_one', 'sub_description_one',
        'sub_title_two', 'sub_description_two',
        'sub_title_three', 'sub_description_three',
        'sub_title_four', 'sub_description_four'
    )


class ProductionContentInline(admin.TabularInline):
    model = ProductionContent
    extra = 1
    fields = ('title', 'description', 'image')


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    inlines = [ProductionContentInline]


@admin.register(DocumentsCertification)
class DocumentsCertificationAdmin(admin.ModelAdmin):
    fields = (
        'title', 'description'
    )


class SustainabilityContentInline(admin.TabularInline):
    model = SustainabilityContent
    extra = 1
    fields = ('title', 'description', 'image')


@admin.register(Sustainability)
class SustainabilityAdmin(admin.ModelAdmin):
    inlines = [SustainabilityContentInline]
    field = ('main_description')
