from modeltranslation.translator import register, TranslationOptions
from .models import ContactInfo

@register(ContactInfo)
class ContactInfoTranslationOptions(TranslationOptions):
    fields = (
        'title_translate', 'description_translate', 
        'aminol_headquarters_translate', 'aminol_factory_translate',
        'registers_translate', 'contact_address_translate'
    )
