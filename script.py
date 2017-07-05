import sys
import logging
import RPi.GPIO as GPIO
from Services import *
from os.path import join
from datetime import datetime, timedelta

global latestTimeScreenUpdate

logging.basicConfig(level=logging.INFO, filename=join(sys.path[0], 'cc.log'), format='%(asctime)s - %(levelname)s - %(message)s')

latestSensorUpdate = datetime.now()
latestTimeScreenUpdate = datetime.now()

logging.info('CC starts')

while True:
    connectedToSlack = True

    if latestSensorUpdate < datetime.now():
        reading = sensor.calculateDistance()
        latestSensorUpdate = datetime.now() + timedelta(seconds=3)
        if reading != False:
            connectedToSlack = slack.messageCheck(reading)
    if latestTimeScreenUpdate < datetime.now() and reading != False:
        screen.drawPage({'level': reading, 'connection': connectedToSlack})
        latestTimeScreenUpdate = datetime.now() + timedelta(seconds=3)

logging.warn('CC stops')
GPIO.cleanup()
