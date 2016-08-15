#Clock Thread Controlling the time

from threading import Thread
import time
import datetime
import pytz


class ClockTread(Thread):

    def __init__(self, timezone="Europe/Berlin"):
        Thread.__init__(self, name="Clock")
        self._stopping = False
        self._play_alarm = False  # currently playing an alarm
        self._timezone = pytz.timezone(timezone)  # default timezone
        self.datetime_now = datetime.datetime.now(self.timezone)
        self.alarm_active = False  # activate alarm
        self._alarm = datetime.datetime.now(self._timezone).replace(hour=8,
                                                                    minute=0)

    def get_current_datetime(self):
        return self.datetime_now

    # return time in a feasible manner
    def get_time_str(self):
        hour = self.datetime_now.hour
        minute = self.datetime_now.minute
        time_str = "{}{}{}{}".format(str(int(hour/10)), str(hour % 10), 
                                     str(int(minute/10)), str(minute % 10))
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
        # TODO stop thread
        while not self._stopping:
            self.datetime_now = datetime.datetime.now(self.timezone)
            time.sleep(1)
            print self.get_time_str()

if __name__ == '__main__':
    clock = ClockTread()
    clock.start()
    time.sleep(1)
    clock.timezone("Europe/London")
    time.sleep(2)
    # print clock.get_current_datetime()
    # print clock.get_time_str()
    #time.sleep(10)
    clock.stop()