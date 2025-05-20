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