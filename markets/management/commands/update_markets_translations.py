from django.core.management.base import BaseCommand
from django.conf import settings
from markets.models import (  
    Markets_Automotive, Markets_Automotive_Content,
    Markets_Industrial, Markets_Industrial_Content,
    Industries_Content, Markets_Shipping, Markets_Shipping_Content
)

class Command(BaseCommand):
    help = 'Copy default values to translation fields for multilingual models'

    def handle(self, *args, **options):
        default_lang = getattr(settings, 'MODELTRANSLATION_DEFAULT_LANGUAGE', 'en')
        languages = [lang_code for lang_code, _ in settings.LANGUAGES]

        def update_instance_fields(instance, fields):
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

        model_configs = [
            (Markets_Automotive, ['title', 'description']),
            (Markets_Automotive_Content, ['title', 'description']),
            (Markets_Industrial, ['title', 'description', 'industries_title', 'industries_description']),
            (Markets_Industrial_Content, ['title', 'description']),
            (Industries_Content, ['title']),
            (Markets_Shipping, ['title', 'description', 'industries_title', 'industries_description']),
            (Markets_Shipping_Content, ['title', 'description']),
        ]

        for model, fields in model_configs:
            for instance in model.objects.all():
                update_instance_fields(instance, fields)
                instance.save()

        self.stdout.write(self.style.SUCCESS("✅ Successfully set translation fields for all multilingual models."))
