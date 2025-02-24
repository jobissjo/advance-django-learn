import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advance_django_learn.settings')

app = Celery('advance_django_learn')

app.config_from_object('django.conf.settings', namespace='CELERY')

app.autodiscover_tasks()

