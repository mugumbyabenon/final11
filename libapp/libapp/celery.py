from __future__ import  absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import timedelta
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libapp.settings')

app = Celery('library')
app.conf.enable_utc = False

app.conf.update(timezone='Africa/Kampala')

app.config_from_object(settings, namespace='CELERY')

#Celery Beat Settings
app.conf.beat_schedule = {
    'send_notification':{
        'task': 'lib.tasks.send_notification',
        'schedule': timedelta(hours=24),
        #'args':
    },

}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
