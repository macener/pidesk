#Clock Thread Controlling the time

import threading
import time
import datetime
import pytz


class ClockTread(threading.Thread):

    def __init__(self, tz="Europe/Berlin"):
        # threading.Thread.__init__(self, name="Clock")
        super(ClockTread, self).__init__(name="Clock")
        self._stopping = False
        self._play_alarm = False  # currently playing an alarm
        self._timezone = pytz.timezone(tz)  # default timezone
        self.timezone_lock = threading.Lock()
        self.datetime_now = datetime.datetime.now(self._timezone)
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
        with self.timezone_lock:
            zone = self._timezone
        return zone

    @timezone.setter
    def timezone(self, zone):
        with self.timezone_lock:
            self._timezone = pytz.timezone(zone)


# TODO set alarm

# TODO get alarm

    # stop the thread execution, time will not be updated any longer
    def stop(self):
        self._stopping = True

    # count clock
    def run(self):
        while not self._stopping:
            with self.timezone_lock:
                self.datetime_now = datetime.datetime.now(self._timezone)
                print self.get_time_str()
                # print self.datetime_now
                time.sleep(1)


if __name__ == '__main__':
    clock = ClockTread()
    clock.start()
    time.sleep(1)
    clock.timezone = "Europe/London"
    time.sleep(1)
    # print clock.get_current_datetime()
    # print clock.get_time_str()
    #time.sleep(10)
    print "Stopping clock"
    clock.stop()
    print "Waiting for clock to terminate"
    clock.join()
    print "clock finished"