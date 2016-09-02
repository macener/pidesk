# A file where all the "wiring" is done, i.e. all the hardware related stuff.
# Kind of a hardware abstraction layer (HAL).
import time
import threading
import sys
if "/home/pi/py_ws/Adafruit_Python_LED_Backpack" not in sys.path:
    sys.path.append("/home/pi/py_ws/Adafruit_Python_LED_Backpack")
from Adafruit_LED_Backpack import SevenSegment


class DisplayThread(threading.Thread):
    def __init__(self, clock):
        super(DisplayThread, self).__init__(name="Display")
        self.segment = SevenSegment.SevenSegment(address=0x70, busnum=1)
        self.stopping = False
        self.segment.begin()
        self.segment.set_brightness(3)
        self.colon = True
        self.clock = clock

    def stop(self):
        self.segment.clear()
        self.segment.write_display()
        self.stopping = True

    def run(self):
        while not self.stopping:

            self.segment.clear()
            self.segment.print_number_str(self.clock.get_time_str())

            # blinking colon
            if self.colon:
                self.segment.set_colon(True)
                self.colon = False
            else:
                self.colon = True

            self.segment.write_display()
            time.sleep(1)
