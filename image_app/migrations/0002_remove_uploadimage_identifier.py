# Generated by Django 4.2.4 on 2023-08-30 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadimage',
            name='identifier',
        ),
    ]
