# Generated by Django 4.1.4 on 2022-12-29 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0007_cocktail_tools'),
    ]

    operations = [
        migrations.AddField(
            model_name='cocktail',
            name='recepie',
            field=models.CharField(default='Recepie here', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cocktail',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
