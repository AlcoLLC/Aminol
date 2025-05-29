from modeltranslation.translator import register, TranslationOptions
from .models import ( Aminol_Official_Dealer,
    Aminol_Official_Dealer_Content, Aminol_Labaratory, Aminol_Logistics
)


@register(Aminol_Official_Dealer)
class AminolOfficialDealerTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'title_description_translate', 'description_translate')


@register(Aminol_Official_Dealer_Content)
class AminolOfficialDealerContentTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(Aminol_Labaratory)
class AminolLabaratoryTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')


@register(Aminol_Logistics)
class AminolLogisticsTranslationOptions(TranslationOptions):
    fields = ('title_translate', 'description_translate')