# Generated by Django 4.1.4 on 2023-01-23 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0013_userstorage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstorage',
            name='user_tools',
        ),
    ]
