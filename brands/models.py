from django.db import models

class Brand_Portal(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='brand_portal/')
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"


class Brand_Portal_Content(models.Model):
    brand_portal = models.ForeignKey(
        Brand_Portal, related_name='brand_portal', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='brand_portal_content/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"