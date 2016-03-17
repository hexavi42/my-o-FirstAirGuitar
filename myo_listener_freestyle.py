import myo as libmyo
import pickle
import copy
import os
from datetime import datetime as dt
import numpy as np


class EmgListen(libmyo.DeviceListener):
    store_data = []

    def on_arm_sync(self, myo, *args):
        print("on_arm_sync")
        myo.set_stream_emg(libmyo.StreamEmg.enabled)

    def on_emg_data(self, myo, timestamp, emg):
        self.store_data.append(emg)


def lblDataDump(data, labels, fName=None, sName=None):
    all_trials = []
    for trial in data:
        trial_data = [[] for channels in trial[0]]
        for channel_no in range(len(np.array(trial).T)):
            trial_data[channel_no].extend(np.array(trial).T[channel_no])
        all_trials.append(trial_data)
    cwd = os.path.dirname(os.path.realpath(__file__))
    sN = os.path.basename(os.path.realpath(__file__)).split('_')[-1]
    if not os.path.isdir("{0}/{1}".format(cwd, "data")):
            os.makedirs("{0}/{1}".format(cwd, "data"))
    dtStr = "{:%y-%m-%d_%H-%M-%S}".format(dt.now())
    if sName:
        sN = sName
    if fName is None:
        fName = "{0}/{1}/{2}_{3}{4}.pkl".format(cwd, "data", dtStr, 'myo-', sN)
    labeled_data = {'data': all_trials, 'labels': labels}
    with open(fName, 'w') as handle:
        pickle.dump(labeled_data, handle)


def main():
    fing_curv = []
    trial_data = []
    libmyo.init()
    listener = EmgListen()
    hub = libmyo.Hub()
    try:
        hub.run_once(1000, listener)
        listener.store_data = []  # clear stored data between runs
        if len(listener.store_data) == 0:  # make sure it's cleared
            print("Run, cleared, and flushed!")
        else:
            raise RuntimeError("store_data cache not flushed!")

        while True:
            print("""Enter the current position of your fingers,\n
            where 0 indicates unbent and x > 0 is some measure of bent,\n
            Separated by spaces, starting with thumb and ending with pinky.\n
            E.g. index finger very bent, rest unbent would be '0 3 0 0 0':""")
            str_fing = raw_input("-->")
            try:
                fing = [int(x) for x in str_fing.split(" ")]
            finally:
                if len(fing) != 5:
                    raise StopIteration("Done Gathering Data")
            raw_input("Form the indicated hand shape. Press Enter when ready.")
            hub.run_once(3000, listener)
            confirm = raw_input("Enter to save or any other input to deny.")
            if confirm == '':
                print("Saved.")
                trial_data.append(copy(listener.store_data).deepcopy())
                fing_curv.append([fing for datum in listener.store_data])
                listener.store_data = []  # clear stored data between runs
                if len(listener.store_data) == 0:  # make sure it's cleared
                    print("Run, cleared, and flushed!")
                else:
                    raise RuntimeError("store_data (len {0}) not flushed!"
                                       .format(len(listener.store_data)))
            else:
                print("Data was not saved.")
    except:
        lblDataDump(trial_data, fing_curv, fName='partial')
        raise
    else:
        lblDataDump(trial_data, fing_curv)
    finally:
        hub.stop(True)
        hub.shutdown()


if __name__ == '__main__':
    main()
