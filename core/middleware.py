from django.middleware.locale import LocaleMiddleware
from django.utils import translation
from django.conf import settings

class CustomLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        if not any(request.path_info.startswith('/' + lang_code + '/') for lang_code, _ in settings.LANGUAGES if lang_code != settings.LANGUAGE_CODE):
            if not request.path_info.startswith('/az/'):
                translation.activate(settings.LANGUAGE_CODE)
                request.LANGUAGE_CODE = translation.get_language()
                return
        
        super().process_request(request)