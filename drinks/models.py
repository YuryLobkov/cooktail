from django.db import models

# Create your models here.
class Cocktail(models.Model):
    name = models.CharField(max_length=30)
    group = models.CharField(max_length = 30)
    volume = models.SmallIntegerField()

    def __str__(self):
        return f'{self.name},{self.group},{self.volume}%'

