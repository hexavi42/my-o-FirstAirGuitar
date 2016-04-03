import myo as libmyo
import numpy as np
import time
import threading
import argparse
from gesture_classifier_5 import nur_net


# https://scimusing.wordpress.com/2013/10/25/ring-buffers-in-pythonnumpy/
# fast ring buffers for computation
class RingBuffer():
    "A 1D ring buffer using numpy arrays"
    def __init__(self, length):
        self.data = np.zeros(length, dtype='f')
        self.index = 0

    def extend(self, x):
        "adds array x to ring buffer"
        x_index = (self.index + np.arange(x.size)) % self.data.size
        self.data[x_index] = x
        self.index = (x_index[-1] + 1) % self.data.size

    def append(self, x):
        "adds element to ring buffer"
        self.data[self.index] = x
        self.index = (self.index + 1) % self.data.size

    def get(self):
        "Returns the first-in-first-out data in the ring buffer"
        idx = (self.index + np.arange(self.data.size)) % self.data.size
        return self.data[idx]


def ringbuff_numpy_test():
    ringlen = 100000
    ringbuff = RingBuffer(ringlen)
    rand = np.random.randn(9999)
    start_time = time.clock()
    for i in range(40):
        ringbuff.extend(rand)  # write
        ringbuff.get()  # read
    print(time.clock() - start_time, "seconds")


class EmgListen(libmyo.DeviceListener):
    store_data = [RingBuffer(30) for channel in range(8)]
    time_stamp = RingBuffer(30)
    prev_x = 0
    prev_mag = 0
    left_myo = None
    right_myo = None

    def on_arm_sync(self, myo, timestamp, arm, x_direction, rotation, warmup_state):
        print("on_arm_sync")
        if arm == arm.left:
            print("left arm connected!")
            self.left_myo = myo.value
            myo.set_stream_emg(libmyo.StreamEmg.enabled)
        elif arm == arm.right:
            print("right arm connected!")
            self.right_myo = myo.value

    def on_emg_data(self, myo, timestamp, emg):
        if myo.value == self.left_myo:
            for channel_no in range(len(emg)):
                self.store_data[channel_no].append(emg[channel_no])
            self.time_stamp.append(timestamp)
        elif myo.value == self.right_myo:
            raise RuntimeError("Right Myo EMG is turned on - not supposed to happen. Did you cross the streams?")

    # change from negative x to positive x is a strum
    def on_accelerometor_data(self, myo, timestamp, acceleration):
        if myo.value == self.left_myo:
            pass
        elif myo.value == self.right_myo:
            if self.prev_x < 0 and acceleration.x > 0:
                channels = [np.mean(np.abs(datum.get())) for datum in self.store_data]
                print("Strum!")
                # insert some code for reacting to a strum here
            self.prev_x = acceleration.x


def main():
    libmyo.init()
    hub = libmyo.Hub()
    hub.run(1000, EmgListen())
    try:
        while hub.running:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print('\nQuit')
    finally:
        hub.shutdown()  # !! crucial


if __name__ == "__main__":
    main()
