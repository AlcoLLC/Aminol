from django.contrib import admin
from .models import Product_group, Segments, Oil_Types, Viscosity, Liter, Product, ProductProperty
from django.utils.html import format_html

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
    
class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 1
    fields = ['property_name', 'unit', 'test_method', 'typical_value', 'order']
    ordering = ['order']

@admin.register(ProductProperty)
class ProductPropertyAdmin(admin.ModelAdmin):
    list_display = ['product', 'property_name', 'unit', 'test_method', 'typical_value', 'order']
    list_filter = ['product', 'unit']
    search_fields = ['property_name', 'test_method', 'product__title']
    list_editable = ['order']
    ordering = ['product', 'order']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_id', 'product_group', 'oil_type', 'has_pds', 'has_sds']
    list_filter = ['product_group', 'segments', 'oil_type', 'viscosity']
    search_fields = ['title', 'product_id', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductPropertyInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'product_id', 'description')
        }),
        ('Specifications', {
            'fields': ('api', 'ilsag', 'acea', 'jaso', 'oem_sertification', 'recommendations')
        }),
        ('Categories', {
            'fields': ('product_group', 'segments', 'oil_type', 'viscosity', 'liters')
        }),
        ('Documents', {
            'fields': ('pds_url', 'sds_url'),
            'classes': ('collapse',),
        }),
    )
    
    def has_pds(self, obj):
        if obj.pds_url:
            return format_html(
                '<a href="{}" target="_blank" class="button">View PDS</a>',
                obj.pds_url
            )
        return '❌'
    has_pds.short_description = 'PDS'
    
    def has_sds(self, obj):
        if obj.sds_url:
            return format_html(
                '<a href="{}" target="_blank" class="button">View SDS</a>',
                obj.sds_url
            )
        return '❌'
    has_sds.short_description = 'SDS'