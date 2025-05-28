from django.core.management.base import BaseCommand
from django.conf import settings
from modeltranslation.utils import get_translation_fields
from about.models import (
    AboutAminol, AboutSectionContent, QualityContent, WeGuarantee,
    ProductionContent, DocumentsCertification, Sustainability, SustainabilityContent
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
            (AboutAminol, ['based_in', 'location', 'exporting_to', 'production_capacity', 'workforce']),
            (AboutSectionContent, ['title', 'description']),
            (QualityContent, ['title', 'description']),
            (WeGuarantee, [
                'title',
                'sub_title_one', 'sub_description_one',
                'sub_title_two', 'sub_description_two',
                'sub_title_three', 'sub_description_three',
                'sub_title_four', 'sub_description_four',
            ]),
            (ProductionContent, ['title', 'description']),
            (DocumentsCertification, ['title', 'description']),
            (Sustainability, ['main_description']),
            (SustainabilityContent, ['title', 'description']),
        ]

        for model, fields in model_configs:
            for instance in model.objects.all():
                update_instance_fields(instance, fields)
                instance.save()

        self.stdout.write(self.style.SUCCESS("Successfully set translation fields for all multilingual models."))
