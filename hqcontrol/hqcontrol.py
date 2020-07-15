import argparse

def _parse_args(parser):
    parser.add_argument('conf', help="config path for daemon mode")
    parser.add_argument('--daemon', help="use daemon mode", action="store_true")
    parser.add_argument('-v',"--verbose", help="increase verbosity", action="store_true")
    return 

def main():
    art="""
      ░░╚══╗░╔═╔════╝
      ╚═╦═╗╠═╩═╩╗╔═╦═╗
      ░░║▒╠╣▒▒▒▒╠╣▒║▒║
      ╔═╩═╝╠═╦═╦╝╚═╩═╝
      ░░╔══╝░╚═╚════╗

    Welcome to HQ Control
    """
    print(art)
    parser = argparse.ArgumentParser()
    _parse_args(parser)
    args= parser.parse_args()

    if(args.daemon):
        if(args.verbose):
            print("Daemon Mode")
    else:
        if(args.verbose):
            print("Script Mode")


if __name__ == "__main__":
    main()
