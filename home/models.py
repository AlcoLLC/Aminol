from django.db import models

class PartnerLogo(models.Model):
    logo = models.ImageField(upload_to='partner_logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MarketLogo(models.Model):
    logo = models.ImageField(upload_to='market_logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CarLogo(models.Model):
    logo = models.ImageField(upload_to='car_logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Gallery Image {self.id}"