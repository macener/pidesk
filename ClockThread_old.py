#ClockThread

import time
import datetime
import pytz
import threading
from Adafruit_LED_Backpack import SevenSegment

class ClockThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.segment = SevenSegment.SevenSegment(address=0x70, busnum=1)
        self.stopping=False
        self.segment.begin()
        self.segment.set_brightness(3)
        self.colon = True

    def stop(self):
        self.segment.clear()
        self.segment.write_display()
        self.stopping=True

    def run(self):
        while(not self.stopping):
            now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
            hour = now.hour

            minute = now.minute
            second = now.second
            #construct a 4 digit time string
            time_str =  str(int(hour/10))+str(hour%10)+str(int(minute/10))\
                        +str(minute%10)
            
            self.segment.clear()
            self.segment.print_number_str(time_str)
            
            #bliking colon
            if self.colon:
                self.segment.set_colon(True)
                self.colon = False
            else:
                self.colon = True
                
            self.segment.write_display()
            time.sleep(1)
