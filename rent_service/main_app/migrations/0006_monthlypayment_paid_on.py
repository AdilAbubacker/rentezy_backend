# Generated by Django 4.2.9 on 2024-01-17 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_rename_payment_date_monthlypayment_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlypayment',
            name='paid_on',
            field=models.DateField(blank=True, null=True),
        ),
    ]
