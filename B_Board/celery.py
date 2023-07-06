import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'B_Board.settings')

app = Celery('B_Board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()