# Generated by Django 5.0.1 on 2024-01-13 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_rename_sent_broadcstnotification_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcstnotification',
            name='broadcast_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
