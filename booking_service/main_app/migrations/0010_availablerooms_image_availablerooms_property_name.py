# Generated by Django 5.0 on 2024-01-16 15:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='availablerooms',
            name='image',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='availablerooms',
            name='property_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
