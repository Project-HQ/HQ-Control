import argparse
import json
from celery import Celery
from .celery import app
import time
from .tasks import execute_script
from redbeat import RedBeatSchedulerEntry as Entry
from redbeat import RedBeatScheduler
from celery.schedules import crontab_parser, crontab
import os
import re
CONFIG = None
HQCORE_URL = None
args= None

def _parse_args(parser):
    """Define cli arguments for hqcontrol
    """
    parser.add_argument('conf', help="config path for daemon mode")
    parser.add_argument('-v',"--verbose", help="increase verbosity", action="store_true")
    parser.add_argument('-f',"--flush", help="flush scheduled tasks", action="store_true")

def _parse_workflow(wf):
    """Define tasks for a workflow in the config
    """
    print(f"Defining Device Listeners for Workflow [{wf['workflow_name']}]")
    schedule = []
    for dlistener in wf["device_listeners"]:
        _handle_device_listener(dlistener)

    print(f"Defining Periodic Tasks for Workflow [{wf['workflow_name']}]")
    for timer in wf["timers"]:
        event =_handle_timer(timer)
        if event is not None:
            schedule.append(event)
    return schedule

def _handle_device_listener(listener):
    """Define a device listener task
    """
    print(f"\tDevice #{listener['device_id']} listens to devices {listener['listen_to_device_ids']} => <{listener['execute']}>")
    #This will eventually turn into a database table listener, for now, it acts instead like the trigger

    insertions = re.findall(r"(?<={{).*?(?=}})", listener["execute"])

    triggered = { # triggered will get passed in as a parameter to the task handler. it is a dictionary of the log entry
        "device_id": 2,
        "id": 4,
        "str_data": "test"
    }

    for raw_insert in insertions:
        insertable = raw_insert.strip()
        if insertable == "log.id":
            # Replace with the log id of the log that triggered the listener
            listener["execute"]=listener["execute"].replace("{{"+raw_insert+"}}",str(triggered["id"]))
        elif insertable == "log.device_id":
            listener["execute"]=listener["execute"].replace("{{"+raw_insert+"}}",str(triggered["device_id"]))
        elif insertable == "log.float_data":
            print(insertable)
        elif insertable == "log.int_data":
            print(insertable)
        elif insertable == "log.str_data":
            print(insertable)
        elif insertable == "log.is_file":
            print(insertable)
        elif insertable == "log.json_data":
            print(insertable)
        else:
            #We weren't able to find what this should be replaced with
            print("Insertion unavailable. use tablename.column to insert data from caught lo, ie: {{log.id}}")
    print("Command after insertions: ", listener["execute"])
    #execute_script.delay(3,listener["execute"])

def _key_to_cache(key):
    """Log new task's key to .task_cache in case something goes wrong and we lose our keys
    """
    with open(".task_cache","a") as f:
        f.write(key+"\n")

def _handle_timer(timer):
    """ Define a cron-based task
    """
    print(f"\tDevice #{timer['device_id']} runs on <{timer['cron']}> => <{timer['execute']}>")
    c = timer["cron"].split()
    schedule =crontab(
        minute= c[0],
        hour= c[1],
        day_of_month= c[2],
        month_of_year= c[3],
        day_of_week= c[4]
    )
    e = Entry(timer['slug'], 'hqcontrol.tasks.execute_script', schedule, args=[timer["device_id"], timer["execute"]], app=app)
    e.save()
    _key_to_cache(e.key.strip())
    return e

def _flush_schedule(schedule):
    """Remove all tasks from redbeat scheduler by key
    """
    new_schedule= []
    if (len(schedule) > 0):
        for entry in schedule:
            try:
               entry.delete()
            except Exception as ex:
                print("Error: ",ex)
                new_schedule.append(entry)
    return new_schedule

def _read_cached_scheduled_tasks():
    """Read in any cached task keys from a previous run if they were left because of a crash
    """
    results = []
    try:
        with open(".task_cache","r") as f:
            for key in f.readlines():
                try:
                    e = Entry.from_key(key.strip(), app=app)
                    if e is not None:
                        results.append(e)
                except Exception as e:
                    print("Task not found: ", e)
    except FileNotFoundError as e:
        return None
    except Exception as e:
        print("Error: ",e)
    return results

def main():
    art="""
        ░░═══╗░╔═╔════▒▒
        ╚═╦═╗╠═╩═╩╗╔═╦═╗
        ░░║▒╠╣▒░▒▒╠╣▒ ▒║
        ╩═╝╠═╦═╦╝╚═╩═╝
        ╔══╝ ╩═╚══╗ 
        ░░═══╝  ░═╩═▒▒░░

    Welcome to HQ Control
    """
    print(art)
    parser = argparse.ArgumentParser()
    _parse_args(parser)
    args= parser.parse_args()

    with open(args.conf) as config_file:
        CONFIG = json.load(config_file)

    HQCORE_URL = f'http://{CONFIG["hq_core_host"]}:{CONFIG["hq_core_port"]}'

    scheduled_entries = _read_cached_scheduled_tasks() # load scheduled entry keys from cache

    if(scheduled_entries is not None):
        print("Flushing any cached schedules..")
        _flush_schedule(scheduled_entries) # we want to clear out tasks before redefining them
        if(args.flush):
            exit()
    else:
        if(args.flush):
            print("No cache found (.task_cache), nothing to flush")

    for workflow in CONFIG["workflows"]:
       scheduled_entries = _parse_workflow(workflow)

    print("\nSetup Complete, start your celery workers. press ctrl+c once to gracefully shutdown.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Removing scheduled tasks...")
        _flush_schedule(scheduled_entries)
        os.remove(".task_cache") # we deleted all of the scheduled tasks, no cache needed
        print("Thank you for using HQ Control")
        exit()

if __name__ == "__main__":
    main()
