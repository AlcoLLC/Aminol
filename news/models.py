from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news/')
    published_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title
    
class News_Content(models.Model):
    news = models.ForeignKey(
        News, related_name='news', on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='news/')

    def __str__(self):
        return f"{self.title}"