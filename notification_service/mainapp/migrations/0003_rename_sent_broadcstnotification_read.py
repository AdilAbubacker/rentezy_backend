# Generated by Django 5.0.1 on 2024-01-12 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_broadcstnotification_user_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='broadcstnotification',
            old_name='sent',
            new_name='read',
        ),
    ]
