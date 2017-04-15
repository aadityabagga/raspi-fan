Scripts to control an externally attached fan to the Raspberry Pi 3.

### Tutorials referred

* http://www.instructables.com/id/Automated-cooling-fan-for-Pi/
* https://hackernoon.com/how-to-control-a-fan-to-cool-the-cpu-of-your-raspberrypi-3313b6e7f92c

### How to use

`control_fan.py` is the script that monitors the temperature and switches the fan on or off as required.

`run_fan.sh` is a script used to start `control_fan.py` and put it in the background.

### Monitoring

(monit)[https://mmonit.com/monit/] can be used to monitor `run_fan.sh` and restart it in case of failure. Example config:

~~~~
check program pifan path "/home/pi/scripts/run_fan.sh status"
  start program = "/home/pi/scripts/run_fan.sh start"
  stop program = "/home/pi/scripts/run_fan.sh stop"
  if status == 1 then restart
~~~~

### See also

(doc/quirks.md)[doc/quirks.md] for some implementation decisions.
