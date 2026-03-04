from django.db import models

class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    media_type = models.CharField(max_length=10, choices=(('image','Image'), ('video','Video')))
    media_url = models.FileField(upload_to='news_media/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title