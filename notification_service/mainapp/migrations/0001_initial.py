# Generated by Django 5.0.1 on 2024-01-12 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BroadcstNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('broadcast_on', models.DateField()),
                ('sent', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-broadcast_on'],
            },
        ),
    ]
