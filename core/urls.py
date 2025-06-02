from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  
]

urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path('', include('about.urls')),
    path('', include('services.urls')),
    path('', include('contact.urls')),
    path('', include('markets.urls')),
    path('', include('faq.urls')),
    path('', include('news.urls')),
    path('', include('brands.urls')),
    path('', include('products.urls')),
    path('', include('career.urls')),
    prefix_default_language=False 
)

urlpatterns += [
    re_path(r'^rosetta/', include('rosetta.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)