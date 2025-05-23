from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('brand_portal/', views.brand_portal_list, name='brand_portal_list'),
    path('brand_portal/<int:pk>/', views.brand_portal_detail, name='brand_portal_detail'),
    path('brand_portal/pdf/<int:content_id>/', views.view_brand_content_pdf, name='view_brand_content_pdf'),

]

