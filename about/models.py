from django.db import models


class AboutAminol(models.Model):
    founded_year = models.IntegerField()
    based_in = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    exporting_to = models.CharField(max_length=200)
    production_capacity = models.CharField(max_length=200)
    workforce = models.CharField(max_length=200)
    shared_image = models.ImageField(upload_to='about/')

    based_in_translate = models.CharField(max_length=200, blank=True, null=True)
    location_translate = models.CharField(max_length=200, blank=True, null=True)
    exporting_to_translate = models.CharField(max_length=200, blank=True, null=True)
    production_capacity_translate = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"About Aminol - Founded {self.founded_year}"


class AboutSectionContent(models.Model):
    about_aminol = models.ForeignKey(
        AboutAminol, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='about_sections/')

    title_translate = models.CharField(max_length=255, blank=True, null=True)
    description_translate = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.title}"


class Quality(models.Model):
    def __str__(self):
        return "Quality Section"


class QualityContent(models.Model):
    quality = models.ForeignKey(
        Quality, related_name='contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='quality/')

    title_translate = models.CharField(max_length=255, blank=True, null=True)
    description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class WeGuarantee(models.Model):
    title = models.CharField(max_length=255, default="We guarantee")
    sub_title_one = models.CharField(max_length=255)
    sub_description_one = models.TextField()
    sub_title_two = models.CharField(max_length=255)
    sub_description_two = models.TextField()
    sub_title_three = models.CharField(max_length=255)
    sub_description_three = models.TextField()
    sub_title_four = models.CharField(max_length=255)
    sub_description_four = models.TextField()

    title_translate = models.CharField(max_length=255, default="We guarantee", blank=True, null=True)
    sub_title_one_translate = models.CharField(max_length=255, blank=True, null=True)
    sub_description_one_translate = models.TextField(blank=True, null=True)
    sub_title_two_translate = models.CharField(max_length=255, blank=True, null=True)
    sub_description_two_translate = models.TextField(blank=True, null=True)
    sub_title_three_translate = models.CharField(max_length=255, blank=True, null=True)
    sub_description_three_translate = models.TextField(blank=True, null=True)
    sub_title_four_translate = models.CharField(max_length=255, blank=True, null=True)
    sub_description_four_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Production(models.Model):
    def __str__(self):
        return "Production Section"


class ProductionContent(models.Model):
    production = models.ForeignKey(
        Production, related_name='contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='production/')

    title_translate = models.CharField(max_length=255, blank=True, null=True)
    description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class DocumentsCertification(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    title_translate = models.CharField(max_length=255, blank=True, null=True)
    description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Sustainability(models.Model):
    main_description = models.TextField()

    main_description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Sustainability Section"


class SustainabilityContent(models.Model):
    sustainability = models.ForeignKey(
        Sustainability, related_name='contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(
        upload_to='sustainability/', blank=True, null=True)
    
    title_translate = models.CharField(max_length=255, blank=True, null=True)
    description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"