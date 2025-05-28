from modeltranslation.translator import register, TranslationOptions
from .models import (
    Brand_Portal, Brand_Portal_Content
)

@register(Brand_Portal)
class BrandPortalTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(Brand_Portal_Content)
class BrandPortalContentTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')
