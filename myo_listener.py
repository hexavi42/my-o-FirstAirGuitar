from time import sleep
from myo import init, Hub, DeviceListener


class Listener(DeviceListener):

    def on_pair(self, myo, timestamp, firmware_version):
        print("Hello, Myo!")

    def on_unpair(self, myo, timestamp):
        print("Goodbye, Myo!")

    def on_orientation_data(self, myo, timestamp, quat):
        print("Orientation:", quat.x, quat.y, quat.z, quat.w)

init()
listener = DeviceListener()
hub = Hub()
hub.run(1000, listener)

try:
    while True:
        sleep(0.5)
finally:
    hub.shutdown()  # !! crucial
