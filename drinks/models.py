from django.db import models

# Create your models here.


class GroupsCocktail(models.Model):
    group_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.group_name}'


class Cocktail(models.Model):
    name = models.CharField(max_length=30)
    group = models.ForeignKey('GroupsCocktail', on_delete=models.CASCADE)
    volume = models.SmallIntegerField()

    def __str__(self):
        return f'{self.name},{self.group},{self.volume}%'

