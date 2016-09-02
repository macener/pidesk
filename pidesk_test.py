
import logging
import sys

if "/home/pi/py_ws/Adafruit_Python_LED_Backpack" not in sys.path:
    sys.path.append("/home/pi/py_ws/Adafruit_Python_LED_Backpack")

log = logging.getLogger('root')
log.setLevel(logging.DEBUG)

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(levelname)8s %(module)15s: %(message)s')
stream.setFormatter(formatter)

log.addHandler(stream)

import time
import datetime
import pytz
import threading
import ClockThread
import Wiring
import AlarmThread

class pidesk:
    def __init__(self):
        self.stopping = False

    def stop(self):
        self.stopping = True

    def run(self):
        log.info("Starting up AlarmPi")

        log.debug("Loading clock")
        clock = ClockThread.ClockThread()
        display = Wiring.DisplayThread(clock)
        alarm = AlarmThread.AlarmThread(clock)
        #clock.setDaemon(True)
        #alarm = AlarmThread.AlarmThread()

        log.debug("Starting clock")
        clock.start()
        display.start()
        alarm.start()

        clock.set_alarm(7,0,day=2)

        # Main loop where we just spin until we receive a shutdown request
        try:
         while(self.stopping is False):
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
         log.warn("Interrupted, shutting down")

        log.warn("Shutting down")
        #media.playVoice('Shutting down. Goodbye')
        time.sleep(2)

        log.info("Stopping all services")

        clock.stop()
        display.stop()
        alarm.stop()

        log.info("Shutdown complete, now exiting")

        time.sleep(2) # To give threads time to shut down

desk = pidesk()
desk.run()
