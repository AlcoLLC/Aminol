from django.db import models

class Aminol_Official_Dealer(models.Model):
    title = models.CharField(max_length=255)
    title_description = models.TextField()
    image = models.ImageField(upload_to='aminol_official_dealer/')
    description = models.TextField()

    title_translate = models.CharField(max_length=255)
    title_description_translate = models.TextField()
    description_translate = models.TextField()

    def __str__(self):
        return f"{self.title}"


class Aminol_Official_Dealer_Content(models.Model):
    aminol_official_dealer = models.ForeignKey(
        Aminol_Official_Dealer, related_name='aminol_official_dealer', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='aminol_official_dealer_content/')

    title_translate = models.CharField(max_length=100)
    description_translate = models.TextField()

    def __str__(self):
        return f"{self.title}"
    
class Aminol_Labaratory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='aminol_labaratory/')

    title_translate = models.CharField(max_length=100)
    description_translate = models.TextField()

    def __str__(self):
        return f"{self.title}"
    
class Aminol_Logistics(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='aminol_logistics/')

    title_translate = models.CharField(max_length=100)
    description_translate = models.TextField()

    def __str__(self):
        return f"{self.title}"