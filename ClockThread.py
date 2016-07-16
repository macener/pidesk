#Clock Thread Controlling the time

from threading import Thread
import time
import datetime
import pytz

class ClockTread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self._stopping = False
        self._play_alarm = False  # currently playing an alarm
        self._alarm_active = False  # activate alarm
        self._timezone = pytz.timezone('Europe/Berlin')  # default timezone

        self.time_now = datetime.datetime.now(self.timezone)
        self._alarm = datetime.datetime.now(self.timezone).replace(hour=8, minute=0)

    def get_current_datetime(self):
        return self.time_now

    # return time in a feasible manner
    def get_time_str(self):
        hour = self.time_now.hour
        minute = self.time_now.minute
        time_str = "{}{}{}{}".format(str(int(hour/10)), str(hour % 10), str(int(minute/10)), str(minute % 10))
        return time_str

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, zone):
        self._timezone = pytz.timezone(zone)

# TODO set alarm
# TODO get alarm

    # stop the thread execution, time will not be updated any longer
    def stop(self):
        self._stopping = True

    # count clock
    def run(self):
        while not self._stopping:
            self.time_now = datetime.datetime.now(self.timezone)
            time.sleep(1)

