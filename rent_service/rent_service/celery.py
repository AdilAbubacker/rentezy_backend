from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rent_service.settings')

# create a Celery instance and configure it using the settings from Django.
app = Celery('rent_service')

# for changing timezone to Asia
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

#Celery Beat Settings
app.conf.beat_schedule = {
    'generate-recurring-paments': {
        'task':'main_app.tasks.generate_recurring_payments',
        # 'schedule': crontab(hour=23, minute=11),  # Run the task on the 1st day of every month at midnight
        'schedule': crontab(minute=0, hour=0, day_of_month=1),  # Run the task on the 1st day of every month at midnight
    },
    'send-rend-reminders': {
        'task':'main_app.tasks.send_rent_reminders',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),  # Run the task on the 1st day of every month at midnight
    },
}

# Discover and configure all modules that are defined in your Django app.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')