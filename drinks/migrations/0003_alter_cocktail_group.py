# Generated by Django 4.1.4 on 2022-12-28 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0002_groupscocktail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cocktail',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drinks.groupscocktail'),
        ),
    ]
