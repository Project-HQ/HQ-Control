# HQ-Control (Python Flavoured!)
Task Manager for HQ-Core

**THIS IS A WORK IN PROGRESS**

If you've come across this repo, feel free to reach out and ask about the project. However, it is not currently ready for use. This message will be removed once we are ready for user testing and review.

**What is example_conf.json?**

This is the example configuration file which HQ Control will run off of. The idea is that someone could run `pip3 install hqcontrol`, write up a config, then type `hqcontrol config.json --daemon` to run the program. 


HQ Control is a smart task scheduler. It can listen for new entries from a device, or trigger on scheduled times. HQ Control will allow you to schedule many tasks asynchronously, allowing you to scale up your workflows as they become more complex. 

**How are tasks scheduled?**

Tasks are scheduled by celery workers. This allows for python to asynchronously schedule tasks for devices and listen for new logs to be executed on.