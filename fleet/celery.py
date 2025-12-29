from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django settings for using Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fleet')

app = Celery('fleet')

# Celery configuration
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
