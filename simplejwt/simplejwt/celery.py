# from __future__ import absolute_import, unicode_literals
import os
# import jwtauth.tasks
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplejwt.settings')

app = Celery('simplejwt')
# app.conf.enable_utc = False

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'send-hello-in-5-minutes':{
        'task': 'jwtauth.tasks.hello',
        'schedule': crontab(minute='*/5'),
        # 'options':{'expires': 300}
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.task(name = "additiona_task")
# def add(x, y):
#     return x+y


#  