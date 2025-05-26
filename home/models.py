from django.db import models

# Create your models here.
class BrandLogo(models.Model):
    logo = models.ImageField(upload_to='brand_logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CarLogos(models.Model):
    logo = models.ImageField(upload_to='car_logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)