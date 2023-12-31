# Generated by Django 5.0 on 2023-12-26 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_availablerooms_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='lease_agreement',
            field=models.FileField(blank=True, null=True, upload_to='lease_agreements/'),
        ),
        migrations.AddField(
            model_name='booking',
            name='monthly_rent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='security_deposit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='stripe_session_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
