import argparse
import json
from celery import Celery
import time
from .tasks import execute_script

app = None
CONFIG = None
HQCORE_URL = None
args= None

def _parse_args(parser):
    parser.add_argument('conf', help="config path for daemon mode")
    parser.add_argument('-v',"--verbose", help="increase verbosity", action="store_true")

def _parse_workflow(wf):
    print(f"Defining Listeners for Workflow[{wf['workflow_name']}]")
    for listener in wf["listeners"]:
        _handle_listener(listener)
    print(f"Defining Timers for Workflow[{wf['workflow_name']}]")
    for timer in wf["timers"]:
        _handle_timer(timer)

def _handle_listener(listener):
    print(f"Device #{listener['device_id']} is assigned to listen to devices {listener['listen_to_device_ids']}, trigger cmd <{listener['execute']}>")

def _handle_timer(timer):
    print(f"Device #{timer['device_id']} is assigned to run on cron schedule <{timer['cron']}>, trigger cmd <{timer['execute']}>")

def main():
    art="""
        ░░═══╗░╔═╔════▒▒
        ╚═╦═╗╠═╩═╩╗╔═╦═╗
        ░░║▒╠╣▒░▒▒╠╣▒ ▒║
        ╩═╝╠═╦═╦╝╚═╩═╝
        ╔══╝ ╩═╚══╗ 
        ░░═╝    ░══▒▒╝ ░░

    Welcome to HQ Control
    """
    print(art)
    parser = argparse.ArgumentParser()
    _parse_args(parser)
    args= parser.parse_args()

    with open(args.conf) as config_file:
        CONFIG = json.load(config_file)
    
    HQCORE_URL = f'http://{CONFIG["hq_core_host"]}:{CONFIG["hq_core_port"]}'

    for workflow in CONFIG["workflows"]:
        _parse_workflow(workflow)

if __name__ == "__main__":
    main()
