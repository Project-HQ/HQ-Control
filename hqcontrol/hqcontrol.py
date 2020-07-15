import argparse
import json
from hqcontrol.tasks import execute_script

def _parse_args(parser):
    parser.add_argument('conf', help="config path for daemon mode")
    parser.add_argument('--daemon', help="use daemon mode", action="store_true")
    parser.add_argument('-v',"--verbose", help="increase verbosity", action="store_true")

def _parse_config(cfg_path):
    with open(cfg_path) as config_file:
        CONFIG = json.load(config_file)
        HQCORE_URL = f'http://{CONFIG["hq_core_host"]}:{CONFIG["hq_core_port"]}'


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

    if(args.daemon):
        if(args.verbose):
            print("Daemon Mode")
        _parse_config(args.conf)
    else:
        if(args.verbose):
            print("Script Mode")

if __name__ == "__main__":
    main()
