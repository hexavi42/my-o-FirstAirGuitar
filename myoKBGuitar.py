import myo as libmyo
import numpy as np
import time
import threading
import argparse
from getch import getch
from doubleMyoGuitar import RingBuffer
from gesture_classifier_5 import nur_net
from gesture_classifier_chords import Category
from play_chords import chord, g_chord, d_chord, em_chord, c_chord

stdChordDict = {'G': g_chord, 'D': d_chord, 'C': c_chord, 'Em': em_chord}

store_data = [RingBuffer(30) for channel in range(8)]
time_stamp = RingBuffer(30)


class EmgListen(libmyo.DeviceListener):
    global store_data
    global time_stamp

    def on_arm_sync(self, myo, *args):
        print("on_arm_sync")
        myo.set_stream_emg(libmyo.StreamEmg.enabled)

    def on_emg_data(self, myo, timestamp, emg):
        for channel_no in range(len(emg)):
            store_data[channel_no].append(emg[channel_no])
        time_stamp.append(timestamp)


def listen():
    libmyo.init()
    listener = EmgListen()
    hub = libmyo.Hub()
    hub.run(1000, listener)
    try:
        while hub.running:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Quitting...")
    finally:
        hub.shutdown()


def main():
    # standard - argparser for arguments and load pickle file
    parser = argparse.ArgumentParser(description='Air Guitar on Myo!')
    parser.add_argument('-f', '--filepath', type=str, default='',
                        help='filepath of weight file to be loaded')
    parser.add_argument('-hl', '--hidden', type=int, default=3,
                        help='number of hidden layers to use in the model')
    parser.add_argument('-w', '--window', type=int, default=30,
                        help='size of moving average window on (100 Hz to 200 Hz expected sampling rate)')
    args = parser.parse_args()
    if args.filepath:
        catter = Category(stdChordDict.keys())
        loaded = nur_net(args.hidden, len(catter.uniques))
        loaded.load(args.filepath)
    else:
        raise Exception("Need to load a neural network - using weights from a file!")
    listener = threading.Thread(target=listen)
    listener.start()
    while True:
        key = str(getch()).upper()
        if key == ' ':
            channels = [np.mean(np.abs(datum.get())) for datum in store_data]
            prediction = loaded.predict(np.array([channels]))
            print(catter.from_categorical(prediction))
            stdChordDict[catter.from_categorical(prediction)].play()
        elif key == 'Q':
            break
        key = str(getch()).upper()


if __name__ == "__main__":
    main()
