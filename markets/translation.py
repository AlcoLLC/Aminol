from modeltranslation.translator import register, TranslationOptions
from .models import (
    Markets_Automotive, Markets_Automotive_Content, Markets_Industrial, 
    Markets_Industrial_Content, Industries_Content, Markets_Shipping, 
    Markets_Shipping_Content
    )


@register(Markets_Automotive)
class MarketsAutomotiveTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(Markets_Automotive_Content)
class MarketsAutomotiveContentTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(Markets_Industrial)
class MarketsIndustrialTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate', 'industries_title_translate', 'industries_description_translate')


@register(Markets_Industrial_Content)
class MarketsIndustrialContentTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(Industries_Content)
class IndustriesContentTranslationOptions(TranslationOptions):
    fields = ('title_translate',)


@register(Markets_Shipping)
class MarketsShippingTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate', 'industries_title_translate', 'industries_description_translate')


@register(Markets_Shipping_Content)
class MarketsShippingContentTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')
