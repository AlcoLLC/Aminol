from django.urls import path, re_path
from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/product-group/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('products/segment/<slug:segment_slug>/', views.product_list, name='product_list_by_segment'),
    path('products/oil-type/<slug:oil_type_slug>/', views.product_list, name='product_list_by_oil_type'),
    path('products/viscosity/<slug:viscosity_slug>/', views.product_list, name='product_list_by_viscosity'),
    path('products/product-group/<slug:category_slug>/segment/<slug:segment_slug>/', views.product_list, name='product_list_by_category_segment'),
    path('products/product-group/<slug:category_slug>/oil-type/<slug:oil_type_slug>/', views.product_list, name='product_list_by_category_oil_type'),
    path('products/product-group/<slug:category_slug>/viscosity/<slug:viscosity_slug>/', views.product_list, name='product_list_by_category_viscosity'),
    path('products/segment/<slug:segment_slug>/oil-type/<slug:oil_type_slug>/', views.product_list, name='product_list_by_segment_oil_type'),
    path('products/segment/<slug:segment_slug>/viscosity/<slug:viscosity_slug>/', views.product_list, name='product_list_by_segment_viscosity'),
    path('products/oil-type/<slug:oil_type_slug>/viscosity/<slug:viscosity_slug>/', views.product_list, name='product_list_by_oil_type_viscosity'),
    path('products/product-group/<slug:category_slug>/segment/<slug:segment_slug>/oil-type/<slug:oil_type_slug>/', views.product_list, name='product_list_by_category_segment_oil_type'),
    path('products/product-group/<slug:category_slug>/segment/<slug:segment_slug>/viscosity/<slug:viscosity_slug>/', views.product_list, name='product_list_by_category_segment_viscosity'),
    path('products/product-group/<slug:category_slug>/oil-type/<slug:oil_type_slug>/viscosity/<slug:viscosity_slug>/', views.product_list, name='product_list_by_category_oil_type_viscosity'),
    path('products/segment/<slug:segment_slug>/oil-type/<slug:oil_type_slug>/viscosity/<slug:viscosity_slug>/', views.product_list, name='product_list_by_segment_oil_type_viscosity'),
    path('products/product-group/<slug:category_slug>/segment/<slug:segment_slug>/oil-type/<slug:oil_type_slug>/viscosity/<slug:viscosity_slug>/', views.product_list, name='product_list_by_all_filters'),
    path('products/search/<str:search_term>/', views.product_search, name='product_search'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('ajax/product-properties/<int:product_id>/', views.product_properties_ajax, name='product_properties_ajax'),
]