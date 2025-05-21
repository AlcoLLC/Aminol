from django.urls import path
from .views import contact_view, contact_page

urlpatterns = [
    path('contactform/', contact_view, name='contact'),
    path('contact/', contact_page, name='contact-page'),
]