from django.core.management.base import BaseCommand
from markets.models import (
    Markets_Automotive, Markets_Automotive_Content,
    Markets_Industrial, Markets_Industrial_Content,
    Industries_Content, Markets_Shipping, Markets_Shipping_Content
)

class Command(BaseCommand):
    help = 'Copy original field values to _translate fields for all market-related models'

    def handle(self, *args, **options):

        def copy_fields(instance, field_pairs):
            updated = False
            for source, target in field_pairs:
                if not getattr(instance, target, None):
                    setattr(instance, target, getattr(instance, source, ''))
                    updated = True
            if updated:
                instance.save()
            return updated

        configs = [
            (Markets_Automotive, [('title', 'title_translate'), ('description', 'description_translate')]),
            (Markets_Automotive_Content, [('title', 'title_translate'), ('description', 'description_translate')]),
            (Markets_Industrial, [
                ('title', 'title_translate'), 
                ('description', 'description_translate'),
                ('industries_title', 'industries_title_translate'),
                ('industries_description', 'industries_description_translate'),
            ]),
            (Markets_Industrial_Content, [('title', 'title_translate'), ('description', 'description_translate')]),
            (Industries_Content, [('title', 'title_translate')]),
            (Markets_Shipping, [
                ('title', 'title_translate'), 
                ('description', 'description_translate'),
                ('industries_title', 'industries_title_translate'),
                ('industries_description', 'industries_description_translate'),
            ]),
            (Markets_Shipping_Content, [('title', 'title_translate'), ('description', 'description_translate')]),
        ]

        total_updated = 0

        for model, fields in configs:
            for instance in model.objects.all():
                if copy_fields(instance, fields):
                    total_updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully updated {total_updated} instances across all market-related models.")
        )
