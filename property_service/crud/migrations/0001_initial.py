# Generated by Django 4.2.7 on 2023-11-23 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('owner_id', models.IntegerField()),
                ('property_type', models.CharField(choices=[('bed', 'Bed'), ('room', 'Room'), ('house', 'House')], max_length=50)),
                ('description', models.TextField()),
                ('image', models.CharField(max_length=255)),
                ('number_of_rooms', models.IntegerField(blank=True, null=True)),
                ('number_of_bathrooms', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud.amenity')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud.property')),
            ],
        ),
    ]