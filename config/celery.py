import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.conf.beat_schedule = {
    'send_mailing': {
        'task': 'mailing.tasks.send_mailing',
        'schedule': crontab(minute='1'),
    },
}