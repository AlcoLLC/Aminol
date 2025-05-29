from modeltranslation.translator import register, TranslationOptions
from .models import (Product_group, Segments,
    Oil_Types, Product, ProductProperty
)

@register(Product_group)
class ProductGroupTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(Segments)
class SegmentsTranslationOptions(TranslationOptions):
    fields = ('title_translate',)


@register(Oil_Types)
class OilTypesTranslationOptions(TranslationOptions):
    fields = ('title_translate',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'title_translate', 'description_translate', 'features_benefits_translate', 'application_translate',
        'recommendations_translate'
    )

@register(ProductProperty)
class ProductPropertyTranslationOptions(TranslationOptions):
    fields = ('property_name_translate', 'unit_translate', 'test_method_translate', 'typical_value_translate')
