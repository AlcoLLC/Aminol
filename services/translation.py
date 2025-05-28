from modeltranslation.translator import register, TranslationOptions
from .models import ( Aminol_Official_Dealer,
    Aminol_Official_Dealer_Content, Aminol_Labaratory, Aminol_Logistics
)


@register(Aminol_Official_Dealer)
class AminolOfficialDealerTranslationOptions(TranslationOptions):
    fields = ('title', 'title_description', 'description')


@register(Aminol_Official_Dealer_Content)
class AminolOfficialDealerContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Aminol_Labaratory)
class AminolLabaratoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Aminol_Logistics)
class AminolLogisticsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')