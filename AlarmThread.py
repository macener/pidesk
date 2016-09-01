#ClockThread

import time
import datetime
import pytz
import threading
import os
from pygame import mixer

class AlarmThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stopping = False
        self.alarmTime = None
        self.playing_alarm = False
        
    def stop(self):
        self.stopping = True
        if self.playing_alarm:
            os.system("mpc stop")

    def playAlarm(self):
        self.playing_alarm = True

        #self.playing_alarm = False
        play = os.system("mpc play 1")
        print play
        #if not play:
        #    mixer.init()
        #    sound = mixer.Sound("/home/pi/Downloads/rain.wav")
        #    sound.play()
        
    def setAlarm(self,alarmTime):
        now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
        time = now.replace(minute=now.minute)
        self.alarmTime = time
        
    def run(self):
        while not self.stopping:
            now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
            if self.alarmTime is not None and not self.playing_alarm \
                and now > self.alarmTime:
                self.playAlarm()
            time.sleep(1)
            
