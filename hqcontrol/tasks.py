from __future__ import absolute_import, unicode_literals
from .celery import app
import time
import shlex
import subprocess
import os

@app.task
def execute_script(device_id, execute_cmd):
    print('execute script')
    try:
        process = subprocess.run(shlex.split(execute_cmd), 
                                    stdout=subprocess.PIPE, 
                                    universal_newlines=True)
        print('script execute finished')
        return {"success":True, "output": process.stdout.strip("")}
    except Exception as e:
        print('script execute failed')
        return {"success":False, "output":str(e)}