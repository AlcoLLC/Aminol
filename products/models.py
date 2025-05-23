from django.db import models

class Product_group(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title
    
class Segments(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title
    
class Oil_Types(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title
    
class Viscosity(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title

class Liter(models.Model):
    volume = models.PositiveIntegerField(unique=True) 

    def __str__(self):
        return f"{self.volume} L"
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    product_id = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    api = models.CharField(max_length=255, blank=True, null=True)
    ilsac = models.CharField(max_length=255, blank=True, null=True)
    acea = models.CharField(max_length=255, blank=True, null=True)
    jaso = models.CharField(max_length=255, blank=True, null=True)
    oem_sertification = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    liters = models.ManyToManyField('Liter', blank=True, related_name='products')
    product_group = models.ForeignKey('Product_group', on_delete=models.CASCADE, related_name='products', null=True)
    segments = models.ForeignKey('Segments', on_delete=models.CASCADE, blank=True, related_name='products', null=True)
    oil_type = models.ForeignKey('Oil_Types', on_delete=models.CASCADE, related_name='products', null=True)
    viscosity = models.ForeignKey('Viscosity', on_delete=models.CASCADE, related_name='products', null=True)
    pds_url = models.URLField(blank=True, null=True, verbose_name="PDS Link")
    sds_url = models.URLField(blank=True, null=True, verbose_name="SDS Link")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class ProductProperty(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='properties')
    property_name = models.CharField(max_length=255, verbose_name="Property")
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name="Unit")
    test_method = models.CharField(max_length=255, verbose_name="Test method")
    typical_value = models.CharField(max_length=100, verbose_name="Typical value")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Product Property'
        verbose_name_plural = 'Product Properties'
    
    def __str__(self):
        return f"{self.product.title} - {self.property_name}"