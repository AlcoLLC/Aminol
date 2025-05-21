from django.db import models
from django.utils import timezone


class Contact(models.Model):
    HELP_CHOICES = [
        ('buy', 'I would like to buy Aminol products'),
        ('info', 'I would like more information'),
        ('other', 'Others'),
    ]
    
    help_type = models.CharField(max_length=50, choices=HELP_CHOICES)
    company_name = models.CharField(max_length=255)
    question = models.TextField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company_name}"
    
class ContactInfo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    aminol_headquarters = models.TextField()
    aminol_headquarters_location = models.URLField(blank=True, help_text="URL for headquarters location (Google Maps link)")
    aminol_factory = models.TextField()
    aminol_factory_location = models.URLField(blank=True, help_text="URL for factory location (Google Maps link)")
    aminol_headquarters_image = models.ImageField(upload_to='aminol_headquarters/')
    aminol_factory_image = models.ImageField(upload_to='aminol_factory/')
    registers = models.TextField()
    contact_address = models.TextField()
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    
    def __str__(self):
        return f"{self.title}"