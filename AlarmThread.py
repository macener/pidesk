#ClockThread

import time
import threading
import os
from pygame import mixer


class AlarmThread(threading.Thread):

    def __init__(self, clock):
        threading.Thread.__init__(self)
        self.stopping = False
        self.alarmTime = None
        self.playing_alarm = False
        self.clock = clock

    def stop(self):
        self.stopping = True
        if self.playing_alarm:
            os.system("mpc stop")

    def play_alarm(self):
        self.playing_alarm = True

        #self.playing_alarm = False
        play = os.system("mpc play 1")
        print play
        #if not play:
        #    mixer.init()
        #    sound = mixer.Sound("/home/pi/Downloads/rain.wav")
        #    sound.play()

    def set_alarm(self, hour, minute):
        self.clock.set_alarm(hour=hour, minute=minute)
        # self.alarmTime = time

    def run(self):
        while not self.stopping:
            if self.clock.alarm_activated and not self.playing_alarm:
                self.playAlarm()
            time.sleep(1)

