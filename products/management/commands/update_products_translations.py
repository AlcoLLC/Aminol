from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import (  
    Product_group, Segments, Oil_Types, Viscosity,
    Product, ProductProperty
)

class Command(BaseCommand):
    help = 'Set default and empty translation fields for Product-related models'

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
            (Product_group, ['title', 'description']),
            (Segments, ['title']),
            (Oil_Types, ['title']),
            (Viscosity, ['title']),
            (Product, ['title', 'description', 'features_benefits', 'application', 'oem_sertification', 'recommendations']),
            (ProductProperty, ['property_name', 'unit', 'test_method', 'typical_value']),
        ]

        for model, fields in models_with_fields:
            for obj in model.objects.all():
                update_fields(obj, fields)
                obj.save()

        self.stdout.write(self.style.SUCCESS("✅ Translation fields for Product-related models set successfully."))
