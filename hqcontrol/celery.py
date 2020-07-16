from __future__ import absolute_import, unicode_literals
from celery import Celery
import json
import os

BROKER_USER = os.environ.get("BROKER_USER","guest")
BROKER_PASSWORD = os.environ.get("BROKER_PASSWORD","guest")
BROKER_HOST = os.environ.get("BROKER_HOST","127.0.0.1")
BROKER_PORT = os.environ.get("BROKER_PORT","5672")
BROKER_VHOST = os.environ.get("BROKER_VHOST","hqcontrol")

CELERY_BROKER_URL=f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}/{BROKER_VHOST}"

app = Celery('hqcontrol',
             broker=CELERY_BROKER_URL,
             backend='rpc://',
             include=['hqcontrol.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)
if __name__ == '__main__':
        app.start()