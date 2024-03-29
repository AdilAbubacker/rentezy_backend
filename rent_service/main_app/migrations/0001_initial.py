# Generated by Django 4.2.9 on 2024-01-10 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RentPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.IntegerField()),
                ('property', models.IntegerField()),
                ('payment_date', models.DateField()),
                ('is_recurring', models.BooleanField(default=True)),
                ('is_paid', models.BooleanField(default=False)),
            ],
        ),
    ]
