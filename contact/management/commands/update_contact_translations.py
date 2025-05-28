from django.core.management.base import BaseCommand
from django.conf import settings
from contact.models import ContactInfo

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
            (ContactInfo, [
                'title', 'description', 'aminol_headquarters', 'aminol_factory',
                'registers', 'contact_address'
            ]),
        ]

        for model, fields in model_configs:
            for instance in model.objects.all():
                update_instance_fields(instance, fields)
                instance.save()

        self.stdout.write(self.style.SUCCESS("Successfully set translation fields for all multilingual models."))
