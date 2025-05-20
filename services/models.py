from django.db import models

class Aminol_Official_Dealer(models.Model):
    title = models.CharField(max_length=255)
    title_description = models.TextField()
    image = models.ImageField(upload_to='aminol_official_dealer/')
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"


class Aminol_Official_Dealer_Content(models.Model):
    aminol_official_dealer = models.ForeignKey(
        Aminol_Official_Dealer, related_name='aminol_official_dealer', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='aminol_official_dealer_content/')

    def __str__(self):
        return f"{self.title}"
    
class Aminol_Labaratory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='aminol_labaratory/')

    def __str__(self):
        return f"{self.title}"
    
class Aminol_Logistics(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='aminol_logistics/')

    def __str__(self):
        return f"{self.title}"