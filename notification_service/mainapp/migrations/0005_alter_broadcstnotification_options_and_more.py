# Generated by Django 5.0.1 on 2024-01-13 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_broadcstnotification_broadcast_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='broadcstnotification',
            options={},
        ),
        migrations.RemoveField(
            model_name='broadcstnotification',
            name='broadcast_on',
        ),
    ]