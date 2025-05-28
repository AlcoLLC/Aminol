from django.core.management.base import BaseCommand
from django.conf import settings
from services.models import ( 
    Aminol_Official_Dealer,
    Aminol_Official_Dealer_Content,
    Aminol_Labaratory,
    Aminol_Logistics,
)

class Command(BaseCommand):
    help = 'Set default and empty translation fields for Aminol Dealer, Labaratory, and Logistics models'

    def handle(self, *args, **options):
        default_lang = getattr(settings, 'MODELTRANSLATION_DEFAULT_LANGUAGE', 'en')
        languages = [lang_code for lang_code, _ in settings.LANGUAGES]

        def update_fields(instance, fields):
            for field in fields:
                default_value = getattr(instance, field, '')
                default_field = f"{field}_{default_lang}"
                if not getattr(instance, default_field, None):
                    setattr(instance, default_field, default_value)
                for lang in languages:
                    if lang != default_lang:
                        translated_field = f"{field}_{lang}"
                        if not getattr(instance, translated_field, None):
                            setattr(instance, translated_field, '')

        models_with_fields = [
            (Aminol_Official_Dealer, ['title', 'title_description', 'description']),
            (Aminol_Official_Dealer_Content, ['title', 'description']),
            (Aminol_Labaratory, ['title', 'description']),
            (Aminol_Logistics, ['title', 'description']),
        ]

        for model, fields in models_with_fields:
            for obj in model.objects.all():
                update_fields(obj, fields)
                obj.save()

        self.stdout.write(self.style.SUCCESS("✅ Aminol translation fields set successfully."))
