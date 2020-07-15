
from celery import Celery
from hqcontrol.hqcontrol import CONFIG

app = Celery('hq_control',
             broker=CONFIG["broker_url"],
             backend='rpc://',
             include=['hqcontrol.tasks'])

