from django.db import models
import os
from uuid import uuid4
from django.contrib.auth.models import User

# Create your models here.


def path_and_rename(instance, filename):
    upload_to = 'cocktails_images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class GroupsCocktail(models.Model):
    group_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.group_name}'


class Ingredients(models.Model):
    class IngTypes(models.TextChoices):
        alc = 'Alc', 'Alcohol'
        soft = 'Sof', 'Soft-drinks'
        garn = 'Gar', 'Garnish'
        other = 'Oth', 'Other'


    name = models.CharField(max_length=30)
    ing_type = models.CharField(max_length=11, choices=IngTypes.choices, default=IngTypes.other)
    description = models.CharField(null=True, max_length=100)


    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField(max_length=30)
    inv_type = models.CharField(max_length=10, choices=
    (('tableware','Tableware'), ('instrument','Instrument'), ('other','Other'))
    )


    def __str__(self):
        return self.name


class Cocktail(models.Model):
    name = models.CharField(max_length=30, unique=True)
    group = models.ForeignKey('GroupsCocktail', on_delete=models.CASCADE)
    volume = models.SmallIntegerField()
    main_ingredients = models.ManyToManyField(Ingredients, related_name='main_ingredients')
    optional_ingredients = models.ManyToManyField(Ingredients, related_name='optional_ingredients')
    tools = models.ManyToManyField(Inventory, related_name='tools')
    recepie = models.CharField(max_length=1000, default='Recepie here')
    image = models.ImageField(null=True, upload_to=path_and_rename, blank=True, default='default.jpg')


    def __str__(self):
        return f'{self.name},{self.group},{self.volume}%'

class UserStorage(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'user_ingredients')

    def __str__(self):
        return f'{self.user_id}, {self.user_ingredients}'


class UserTools(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'user_inventory')

    def __str__(self):
        return f'{self.user}, {self.user_inventory}'
