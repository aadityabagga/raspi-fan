#!/usr/bin/env python
# control_fan.sh: A script to control a fan connected to a raspberry pi

# Based upon the following sources:
# http://www.instructables.com/id/Automated-cooling-fan-for-Pi/
# https://hackernoon.com/how-to-control-a-fan-to-cool-the-cpu-of-your-raspberrypi-3313b6e7f92c

##
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed WITHOUT ANY WARRANTY;
#  without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import os
import time
import signal
import sys
import RPi.GPIO as GPIO

# The pin ID (https://www.raspberrypi.org/documentation/usage/gpio/README.md)
PIN = 15
# Start fan if temp > start temp
FAN_START = 58
# Stop fan if temp < end temp
FAN_END = 47
# Time to wait for before switching fan on / off
WAIT_INTERVAL = 30

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, GPIO.LOW)
    return()

def get_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp = (res.replace("temp=","").replace("'C\n",""))
    return temp

def fanON():
    GPIO.setup(PIN, GPIO.OUT)
    setPin(GPIO.HIGH)
    return()

def fanOFF():
    setPin(GPIO.LOW)
    GPIO.setup(PIN, GPIO.IN)
    return()

def run():
    temp = get_temperature()
    CPU_temp = float(temp)
    print(time.strftime('%Y-%m-%d %X') + ' , temp is ' + temp)
    if CPU_temp > FAN_START:
        if check_fan(PIN) != GPIO.HIGH:
            print('Turning fan on')
        # Since the input read can be wrong, run the function nevertheless
        fanON()
    elif CPU_temp < FAN_END:
        if check_fan(PIN) == GPIO.HIGH:
            print('Turning fan off')
        fanOFF()
    else:
        # nothing to do
        pass
    #print check_fan(PIN)
    return()

def setPin(mode):
    GPIO.output(PIN, mode)
    return()

def check_fan(pin):
    return GPIO.input(pin)

def cleanUP():
    GPIO.cleanup()

# Get the action. For manually turning on/off the fan
action = sys.argv.pop()

if action == "on" or action == "start":
    print "Turning fan on"
    setup()
    fanON()
    exit()
elif action == "off" or action == "stop":
    print "Turning fan off"
    setup()
    fanOFF()
    exit()
elif action == "status":
    temp = get_temperature()
    print('Temp is ' + temp)
    CPU_temp = float(temp)
    if CPU_temp > FAN_START:
        print('Fan should be on')
    elif CPU_temp < FAN_END:
        print('Fan should be off')
    else:
        print('Fan state unknown')
    exit()

# Handle signal (http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python)
signal.signal(signal.SIGINT, signal.default_int_handler)

try:
    setup()
    while True:
        run()
        time.sleep(WAIT_INTERVAL)
except KeyboardInterrupt:
    # trap a CTRL+C keyboard interrupt
    # resets all GPIO ports used by this program
    GPIO.cleanup()
finally:
    GPIO.cleanup()
