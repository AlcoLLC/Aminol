from django.core.management.base import BaseCommand
from django.conf import settings
from brands.models import Brand_Portal, Brand_Portal_Content 

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
            (Brand_Portal, ['title', 'description']),
            (Brand_Portal_Content, ['title', 'description']),
        ]

        for model, fields in model_configs:
            for instance in model.objects.all():
                update_instance_fields(instance, fields)
                instance.save()

        self.stdout.write(self.style.SUCCESS("Successfully set translation fields for all multilingual models."))
