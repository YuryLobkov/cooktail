# Generated by Django 4.1.4 on 2023-01-05 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0009_cocktail_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cocktail',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cocktails_images'),
        ),
    ]
