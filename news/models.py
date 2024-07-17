from django.db import models

# Create your models here.
class News(models.Model):
    news_title = models.CharField(max_length=120)
    news = models.TextField()

    def __str__(self):
        return self.news_title

