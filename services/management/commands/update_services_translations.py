from django.core.management.base import BaseCommand
from services.models import ( 
    Aminol_Official_Dealer,
    Aminol_Official_Dealer_Content,
    Aminol_Labaratory,
    Aminol_Logistics,
)

class Command(BaseCommand):
    help = 'Copy original fields into *_translate fields for Aminol models'

    def handle(self, *args, **options):
        def copy_fields(instance, field_pairs):
            updated = False
            for original, translated in field_pairs:
                if not getattr(instance, translated, None):
                    setattr(instance, translated, getattr(instance, original, ''))
                    updated = True
            if updated:
                instance.save()
            return updated

        updated_counts = {
            "Aminol_Official_Dealer": 0,
            "Aminol_Official_Dealer_Content": 0,
            "Aminol_Labaratory": 0,
            "Aminol_Logistics": 0,
        }

        for item in Aminol_Official_Dealer.objects.all():
            if copy_fields(item, [
                ('title', 'title_translate'),
                ('title_description', 'title_description_translate'),
                ('description', 'description_translate'),
            ]):
                updated_counts["Aminol_Official_Dealer"] += 1

        for item in Aminol_Official_Dealer_Content.objects.all():
            if copy_fields(item, [
                ('title', 'title_translate'),
                ('description', 'description_translate'),
            ]):
                updated_counts["Aminol_Official_Dealer_Content"] += 1

        for item in Aminol_Labaratory.objects.all():
            if copy_fields(item, [
                ('title', 'title_translate'),
                ('description', 'description_translate'),
            ]):
                updated_counts["Aminol_Labaratory"] += 1

        for item in Aminol_Logistics.objects.all():
            if copy_fields(item, [
                ('title', 'title_translate'),
                ('description', 'description_translate'),
            ]):
                updated_counts["Aminol_Logistics"] += 1

        self.stdout.write(self.style.SUCCESS("✅ Aminol translations copied successfully."))
        for model, count in updated_counts.items():
            self.stdout.write(f"  - {model}: {count} updated")
