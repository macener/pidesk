#Clock Thread Controlling the time

import threading
import time
import datetime
import pytz


class ClockThread(threading.Thread):

    def __init__(self, tz="Europe/Berlin"):
        super(ClockThread, self).__init__(name="Clock")
        self._stopping = False
        self._play_alarm = False  # currently playing an alarm

        self._timezone = pytz.timezone(tz)  # default timezone
        self.timezone_lock = threading.Lock()

        self._datetime_now = datetime.datetime.now(self._timezone)
        self.datetime_lock = threading.Lock()

        self._alarm_set = False  # activate alarm
        self.alarm_set_lock = threading.Lock()

        self._alarm_activated = False
        self.alarm_activated_lock = threading.Lock()

        self._alarm_datetime = datetime.datetime.now(self._timezone).\
            replace(hour=10, minute=0, second=0, microsecond=0)
        self.alarm_lock = threading.Lock()

    @property
    def datetime_now(self):
        with self.datetime_lock:
            datetime_now = self._datetime_now
        return datetime_now

    @datetime_now.setter
    def datetime_now(self, datetime_now):
        with self.datetime_lock:
            self._datetime_now = datetime_now

    # return time in a feasible manner
    def get_time_str(self):
        time_now = self.datetime_now  # thread safe call of datetime_now
        hour = time_now.hour
        minute = time_now.minute
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

    @property
    def alarm_datetime(self):
        with self.alarm_lock:
            alarm_time = self._alarm_datetime
        return alarm_time

    @alarm_datetime.setter
    def alarm_datetime(self, datetime_ins):
        # TODO change assert to log entry and return
        assert isinstance(datetime_ins, datetime.datetime), \
            "Datetime has wrong format"
        with self.alarm_lock:
            self._alarm_datetime = datetime_ins

    def set_alarm(self, hour, minute, day=None, month=None, year=None):

        assert 0 <= minute < 60
        assert 0 <= hour < 60
        with self.alarm_lock and self.alarm_set_lock:
            alarm = self._alarm_datetime
            alarm = alarm.replace(minute=minute, hour=hour)

            if month is not None:
                alarm = alarm.replace(month=month)
            if year is not None:
                alarm = alarm.replace(year=year)
            if day is not None:
                alarm = alarm.replace(day=day)
            elif alarm < self._alarm_datetime:
                # set alarm to next morning
                tomorrow = datetime.date.today()+datetime.timedelta(days=1)
                alarm = alarm.replace(year=tomorrow.year,
                                      month=tomorrow.month, day=tomorrow.day)
            self._alarm_datetime = alarm
            # activate alarm, because if you set it, you want to have it
            # going off, believe me
            self._alarm_set = True

    @property
    def alarm_set(self):
        with self.alarm_set_lock:
            set = self._alarm_set
        return set

    @alarm_set.setter
    def alarm_set(self, set):
        assert isinstance(set, bool), "set needs be of type bool"
        with self.alarm_set_lock:
            self._alarm_set = set

    @property
    def alarm_activated(self):
        with self.alarm_activated_lock:
            active = self._alarm_activated
        return active

    @alarm_activated.setter
    def alarm_activated(self, active):
        assert isinstance(active, bool), "active needs be of type bool"
        with self.alarm_activated_lock:
            self._alarm_activated = active


    # stop the thread execution, time will not be updated any longer
    def stop(self):
        self._stopping = True

    # count clock
    def run(self):
        while not self._stopping:
            # access class variables via properties in order to ensure
            # thread safety
            self.datetime_now = datetime.datetime.now(self.timezone)
            # print self.get_time_str()
            if self.alarm_set and self.datetime_now > self.alarm_datetime:
                self.alarm_activated = True
            # print self.datetime_now
            # print self.alarm_activated
            time.sleep(1)


if __name__ == '__main__':
    # ClockTread Testbench
    clock = ClockTread()
    clock.start()
    # time.sleep(1)
    clock.timezone = "Europe/London"
    time.sleep(1)
    clock.timezone = "Europe/Amsterdam"
    time.sleep(1)
    clock.timezone = "US/Eastern"
    time.sleep(1)
    clock.timezone = "Europe/Berlin"
    clock.set_alarm(21,42)
    time.sleep(45)
    print clock.alarm_datetime
    # print clock.get_current_datetime()
    # print clock.get_time_str()
    # time.sleep(10)
    print "Stopping clock"
    clock.stop()
    print "Waiting for clock to terminate"
    clock.join()
    print "clock finished"
