from django.db import models

# Create your models here.


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


class Cocktail(models.Model):
    name = models.CharField(max_length=30)
    group = models.ForeignKey('GroupsCocktail', on_delete=models.CASCADE)
    volume = models.SmallIntegerField()
    main_ingredients = models.ManyToManyField(Ingredients)


    def __str__(self):
        return f'{self.name},{self.group},{self.volume}%'

