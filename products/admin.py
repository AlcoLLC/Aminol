from django.contrib import admin
from .models import Product_group, Segments, Oil_Types, Viscosity, Liter, Product


@admin.register(Product_group)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Segments)
class SegmentsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Oil_Types)
class OilTypesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Viscosity)
class ViscosityAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Liter)
class LiterAdmin(admin.ModelAdmin):
    list_display = ('volume',)
    ordering = ('volume',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_id', 'product_group', 'oil_type', 'viscosity', 'created_at')
    list_filter = ('product_group', 'oil_type', 'viscosity', 'segments', 'created_at')
    search_fields = ('title', 'product_id', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['liters']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'product_id', 'slug')
        }),
        ('Classification', {
            'fields': ('product_group', 'segments', 'oil_type', 'viscosity')
        }),
        ('Specifications', {
            'fields': ('api', 'ilsag', 'acea', 'jaso', 'oem_sertification', 'reccommendations')
        }),
        ('Available Sizes', {
            'fields': ('liters',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product_group', 'oil_type', 'viscosity')