from django.db import models
from django.utils import timezone

# Create your models here.
class Person(models.Model):
    name = models.TextField(max_length=200)
    age = models.IntegerField()
    hobby = models.TextField(blank=True, max_length=200)
    birthday = models.DateTimeField(blank=True, null=True)
    

    def publish(self):
        self.birthday = timezone.now()
        self.save()

    def __str__(self):
        return self.name