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


    def __str__(self):
        return self.name


class Cocktail(models.Model):
    #id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=30, unique=True)
    group = models.ForeignKey('GroupsCocktail', on_delete=models.CASCADE)
    volume = models.SmallIntegerField()
    main_ingredients = models.ManyToManyField(Ingredients, related_name='main_ingredients')
    optional_ingredients = models.ManyToManyField(Ingredients, related_name='optional_ingredients')
    tools = models.ManyToManyField(Inventory, related_name='tools')
    recepie = models.CharField(max_length=1000, default='Recepie here')
    image = models.ImageField(null=True, upload_to='cocktails_images', blank=True)


    def __str__(self):
        return f'{self.name},{self.group},{self.volume}%'

