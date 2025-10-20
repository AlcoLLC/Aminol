from modeltranslation.translator import register, TranslationOptions, translator
from .models import (Product_group, Segments,
    Oil_Types, Product, ProductProperty, Product_Group_Category
)

@register(Product_group)
class ProductGroupTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate', 'meta_title', 'meta_description')


@register(Segments)
class SegmentsTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'meta_title', 'meta_description')


@register(Oil_Types)
class OilTypesTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'meta_title', 'meta_description')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'title_translate', 'description_translate', 'features_benefits_translate', 'application_translate',
        'recommendations_translate', 'meta_title', 'meta_description', 'meta_keywords'
    )

@register(ProductProperty)
class ProductPropertyTranslationOptions(TranslationOptions):
    fields = ('property_name_translate', 'unit_translate', 'test_method_translate', 'typical_value_translate')

class ProductGroupCategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(Product_Group_Category, ProductGroupCategoryTranslationOptions)