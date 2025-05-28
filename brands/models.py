from django.db import models

class Brand_Portal(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='brand_portal/')
    description = models.TextField()

    title_translate = models.CharField(max_length=255)
    description_translate = models.TextField()

    def __str__(self):
        return f"{self.title}"


class Brand_Portal_Content(models.Model):
    brand_portal = models.ForeignKey(
        Brand_Portal, related_name='brand_portal', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='brand_portal_content/')
    pdf = models.FileField(upload_to='brand_portal_pdfs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title_translate = models.CharField(max_length=100)
    description_translate = models.TextField()

    def __str__(self):
        return f"{self.title}"