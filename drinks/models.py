from django.db import models

# Create your models here.
class cocktail(models.Model):
    name = models.CharField(max_length=30)
    group = models.CharField(max_length = 30)
    volume = models.SmallIntegerField()

