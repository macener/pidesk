"""
main entry for pidesk
takes some inspiration from mattdy's alarmpi
"""
import logging
import sys
import time
import ClockThread
import Wiring
import AlarmThread

log = logging.getLogger('root')
log.setLevel(logging.DEBUG)

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)8s %(module)15s: %(message)s')
stream.setFormatter(formatter)

log.addHandler(stream)


class piDesk:
    def __init__(self):
        self.stopping = False

    def stop(self):
        self.stopping = True

    def run(self):
        log.info("Starting pidesk")

        log.debug("Loading clock")
        clock = ClockThread.ClockThread()
        display = Wiring.DisplayThread(clock)
        alarm = AlarmThread.AlarmThread(clock)

        log.debug("Starting clock")
        clock.start()
        display.start()
        alarm.start()

        clock.set_alarm(22,20)

        # Main loop where we just spin until we receive a shutdown request
        try:
            while self.stopping is False:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            log.warn("Interrupted, shutting down")

        log.warn("Shutting down")
        time.sleep(2)

        log.info("Stopping all services")

        clock.stop()
        display.stop()
        alarm.stop()

        # wait unitl threads have terminated
        clock.join()
        display.join()
        alarm.join()

        log.info("Shutdown complete, now exiting")

desk = piDesk()
desk.run()
