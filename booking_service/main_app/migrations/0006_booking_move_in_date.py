# Generated by Django 5.0 on 2024-01-06 03:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_booking_stripe_charge_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='move_in_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]