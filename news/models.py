from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news/')
    published_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    title_translate = models.CharField(max_length=255, blank=True, null=True)
    content_translate = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title
    
class News_Content(models.Model):
    news = models.ForeignKey(
        News, related_name='contents', on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='news/')

    description_translate = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.news.title} Content"
