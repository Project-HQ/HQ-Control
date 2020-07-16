from __future__ import absolute_import, unicode_literals
from celery import Celery
import json
import os

BROKER_USER = os.environ.get("BROKER_USER","")
BROKER_PASSWORD = os.environ.get("BROKER_PASSWORD","")
BROKER_HOST = os.environ.get("BROKER_HOST","127.0.0.1")
BROKER_PORT = os.environ.get("BROKER_PORT","6379")
BROKER_VHOST = os.environ.get("BROKER_VHOST","0")

BROKER_URL=f"redis://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}/{BROKER_VHOST}"
CELERYBEAT_SCHEDULER = 'redbeat.RedBeatScheduler'
CELERYBEAT_MAX_LOOP_INTERVAL = 5  # redbeat likes fast loops

app = Celery('hqcontrol',
             broker=BROKER_URL,
             backend='rpc://',
             include=['hqcontrol.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
        app.start()
