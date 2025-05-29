from modeltranslation.translator import register, TranslationOptions
from .models import (
    AboutAminol, AboutSectionContent, QualityContent, WeGuarantee,
    ProductionContent, DocumentsCertification, Sustainability, SustainabilityContent
)

from django.utils import translation
translation.activate('en')


@register(AboutAminol)
class AboutAminolTranslationOptions(TranslationOptions):
    fields = ('based_in_translate', 'location_translate', 'exporting_to_translate', 'production_capacity_translate')


@register(AboutSectionContent)
class AboutSectionContentTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(QualityContent)
class QualityContentTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(WeGuarantee)
class WeGuaranteeTranslationOptions(TranslationOptions):
    fields = (
        'title_translate', 'sub_title_one_translate', 'sub_description_one_translate',
        'sub_title_two_translate', 'sub_description_two_translate',
        'sub_title_three_translate', 'sub_description_three_translate',
        'sub_title_four_translate', 'sub_description_four_translate'
    )


@register(ProductionContent)
class ProductionContentTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(DocumentsCertification)
class DocumentsCertificationTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(Sustainability)
class SustainabilityTranslationOptions(TranslationOptions):
    fields = ('main_description_translate',)


@register(SustainabilityContent)
class SustainabilityContentTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')