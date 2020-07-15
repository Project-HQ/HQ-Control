from hqcontrol.celery import app
import time

@app.task
def execute_script(device_id, execute_cmd):
    print('execute script')
    # sleep 5 seconds
    time.sleep(5)
    print('script execute finished')
    return {"success":True}