from django.urls import path
from .views import home_view, contact_view, brand_portal_view, faq_view, news_view, career_view


urlpatterns = [
    path("", home_view),
    path('contact/', contact_view, name='contact'),
    path('brand_portal/', brand_portal_view, name='brand_portal'),
    path('faq/', faq_view, name='faq'),
    path('news/', news_view, name='news'),
    path('career/', career_view, name='career'),
]