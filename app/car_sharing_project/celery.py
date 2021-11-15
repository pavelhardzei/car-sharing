import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_sharing_project.settings')

app = Celery('car_sharing_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
