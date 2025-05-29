from django.core.management.base import BaseCommand
from contact.models import ContactInfo

class Command(BaseCommand):
    help = 'Copy default field values to _translate fields for ContactInfo model'

    def handle(self, *args, **options):

        def update_instance_fields(instance, field_pairs):
            for original_field, translate_field in field_pairs:
                original_value = getattr(instance, original_field, '')
                if not getattr(instance, translate_field, None):
                    setattr(instance, translate_field, original_value)

        field_mappings = [
            ('title', 'title_translate'),
            ('description', 'description_translate'),
            ('aminol_headquarters', 'aminol_headquarters_translate'),
            ('aminol_factory', 'aminol_factory_translate'),
            ('registers', 'registers_translate'),
            ('contact_address', 'contact_address_translate'),
        ]

        for instance in ContactInfo.objects.all():
            update_instance_fields(instance, field_mappings)
            instance.save()

        self.stdout.write(self.style.SUCCESS("Successfully copied values to _translate fields in ContactInfo."))
