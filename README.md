# HQ-Control (Python Flavoured!)
Task Manager for HQ-Core

**THIS IS A WORK IN PROGRESS**

If you've come across this repo, feel free to reach out and ask about the project. However, it is not currently ready for use. This message will be removed once we are ready for user testing and review.

## What is this?

HQ Control is a smart task scheduler for HQ Core. It can listen for new entries from a device, or trigger on scheduled times. HQ Control will allow you to schedule many tasks asynchronously, allowing you to scale up your workflows as they become more complex.

## How to run

- Start a redis server
- Start an HQ Core server
- Register your devices and clusters on HQ Core
- Create your config based off example_conf.json
- Enter needed environment variables for broker:
    ```
        BROKER_USER = (Default "")
        BROKER_PASSWORD = (Default "")
        BROKER_HOST = (Default "127.0.0.1")
        BROKER_PORT = (Default "6379")
        BROKER_VHOST = (Default "0")
    ```

Run hq-control, passing path to config: `hqcontrol conf.json`

Start Celery Worker: `celery -A hqcontrol worker -l info`

Start Celery Beat: `celery beat -A hqcontrol -l info -S redbeat.RedBeatScheduler`

**Setup Tip**

- Run flower to monitor transactions: `flower -A hqcontrol --port=5555`

- Tasks are flushed at the start of each hqcontrol instance to avoid duplicates, but if something closes unexpectedly, you can also clear your cache of instances that are still scheduled using `hqcontrol conf.json --flush`
  
**What is example_conf.json?**

This is the example configuration file which HQ Control will run off of. The idea is that someone could run `pip3 install hqcontrol`, write up a config, then type `hqcontrol config.json --daemon` to run the program.  

**How are tasks scheduled?**

Tasks are scheduled by celery workers. This allows for python to asynchronously schedule tasks for devices and listen for new logs to be executed on.
