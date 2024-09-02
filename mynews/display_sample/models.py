from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class News(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    publish_date = models.DateField(auto_now=False, auto_now_add=False)
    
    def save_news(self):
        if self.publish_date is None:
            self.publish_date = timezone.now()
        self.save()