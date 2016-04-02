#!/usr/bin/env python

from time import sleep
from myo import init, Hub, DeviceListener

class Listener(DeviceListener):

    def __init__(self):
        self.prev_x = 0
        self.prev_mag = 0

    def on_pair(self, myo, timestamp, firmware_version):
        print("Hello, Myo!")

    def on_unpair(self, myo, timestamp):
        print("Goodbye, Myo!")

    # change from negative x to positive x is a strum
    def on_accelerometor_data(self, myo, timestamp, acceleration):
        if self.prev_x < 0 and acceleration.x > 0:
            print("Strummed")
        self.prev_x = acceleration.x

init()
hub = Hub()
hub.run(1000, Listener())
try:
    while hub.running:
        sleep(0.5)
except KeyboardInterrupt:
    print('\nQuit')
finally:
    hub.shutdown()  # !! crucial
