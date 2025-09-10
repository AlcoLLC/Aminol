from modeltranslation.translator import register, TranslationOptions
from .models import News, News_Content

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'content_translate', 'meta_title', 'meta_description', 'meta_keywords')


@register(News_Content)
class NewsContentTranslationOptions(TranslationOptions):
    fields = ('description_translate',)

