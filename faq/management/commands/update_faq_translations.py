from django.core.management.base import BaseCommand
from faq.models import FAQ
from django.conf import settings

class Command(BaseCommand):
    help = 'Copy default values to translation fields for existing FAQs'
    
    def handle(self, *args, **kwargs):
        default_lang = getattr(settings, 'MODELTRANSLATION_DEFAULT_LANGUAGE', 'en')
        
        for faq in FAQ.objects.all():
            if not getattr(faq, f'question_{default_lang}', None):
                setattr(faq, f'question_{default_lang}', faq.question)
            if not getattr(faq, f'answer_{default_lang}', None):
                setattr(faq, f'answer_{default_lang}', faq.answer)
            
            for lang_code, lang_name in settings.LANGUAGES:
                if lang_code != default_lang:
                    if not getattr(faq, f'question_{lang_code}', None):
                        setattr(faq, f'question_{lang_code}', '')  
                    if not getattr(faq, f'answer_{lang_code}', None):
                        setattr(faq, f'answer_{lang_code}', '')  
            
            faq.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated translation fields for {FAQ.objects.count()} FAQs.'
            )
        )