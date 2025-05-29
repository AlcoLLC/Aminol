from django.db import models

class Markets_Automotive(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='markets_automotive/')
    description = models.TextField()

    title_translate = models.CharField(max_length=255, blank=True, null=True)
    description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class Markets_Automotive_Content(models.Model):
    markets_automotive = models.ForeignKey(
        Markets_Automotive, related_name='automotive_contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='markets_automotive_content/')

    title_translate = models.CharField(max_length=255, blank=True, null=True)
    description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
    
class Markets_Industrial(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='markets_industrial/')
    description = models.TextField()
    industries_title = models.CharField(max_length=255)
    industries_description = models.TextField()
    
    title_translate = models.CharField(max_length=255, blank=True, null=True)
    description_translate = models.TextField(blank=True, null=True)
    industries_title_translate = models.CharField(max_length=255, blank=True, null=True)
    industries_description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class Markets_Industrial_Content(models.Model):
    markets_industrial = models.ForeignKey(
        Markets_Industrial, related_name='industrial_contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='markets_industrial_content/')

    title_translate = models.CharField(max_length=100)
    description_translate = models.TextField()

    def __str__(self):
        return f"{self.title}"
    
class Industries_Content(models.Model):
    markets_industrial = models.ForeignKey(
        Markets_Industrial, related_name='industry_items', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    title_translate = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

class Markets_Shipping(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='markets_shipping/') 
    description = models.TextField()
    industries_title = models.CharField(max_length=255)
    industries_description = models.TextField()

    title_translate = models.CharField(max_length=255, blank=True, null=True)
    description_translate = models.TextField(blank=True, null=True)
    industries_title_translate = models.CharField(max_length=255, blank=True, null=True)
    industries_description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class Markets_Shipping_Content(models.Model):
    markets_shipping = models.ForeignKey( 
        Markets_Shipping, related_name='shipping_contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='markets_shipping_content/') 

    title_translate = models.CharField(max_length=100, blank=True, null=True)
    description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"