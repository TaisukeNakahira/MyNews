from django.db import models
from django.utils import timezone

# Create your models here.
class Articles(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    publish_date = models.DateField(default=timezone.now, auto_now=False, auto_now_add=False, null=True)
    site = models.CharField(max_length=200, null=True)
    like = models.BooleanField(default=False, null=False)
    
    def save_article(self):
        self.save()
    
    def __str__(self):
        return self.title

class Favorites(models.Model):
    article = models.OneToOneField(Articles, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    
    def save_favorite(self):
        self.save()
    
    # def __str__(self):
    #     return self.article.title