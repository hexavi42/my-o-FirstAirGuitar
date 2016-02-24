import myo as libmyo
import pickle
import copy

fing_curv = []
trial_data = []


class EmgListen(libmyo.DeviceListener):
    store_data = []

    def on_arm_sync(self, myo, *args):
        print("on_arm_sync")
        myo.set_stream_emg(libmyo.StreamEmg.enabled)

    def on_emg_data(self, myo, timestamp, emg):
        self.store_data.append(emg)


def dump(data, labels, file="myo_data.pkl"):
    labeled_data = {"data": data, "labels": labels}
    with open(file, 'w') as handle:
        pickle.dump(labeled_data, handle)


def main():
    libmyo.init()
    listener = EmgListen()
    hub = libmyo.Hub()
    try:
        hub.run_once(1000, listener)
        listener.store_data = []
        if len(listener.store_data) == 0:
            print "Run, cleared, and flushed!"
        else:
            raise RuntimeError("store_data cache not flushed!")

        # while True:
            # print("""Enter the current position of your fingers,\n
            # where 1 indicates bent and 0 indicates unbent,\n
            # Separated by spaces, starting with thumb and ending with pinky.\n
            # E.g. index finger bent, rest unbent would be '0 1 0 0 0':"""
            # str_fing = raw_input("-->")
            # try:
            #     fing = [int(x) for x in str_fing.split(" ")]
            # finally:
            #     if len(fing) != 5 or len(set(fing)) > 2 or max(fing) > 1 or min(fing) < 0:
            #         raise StopIteration("Done Gathering Data")

        print("""Bend your fingers as indicated by the printed array\n
        where 1 indicates bent and 0 indicates unbent,\n
        "starting with your thumb and ending with your pinky.\n
        "E.g. index finger bent, the rest unbent would be '01000':\n""")

        for n in range(32):
            print(list('{0:05b}'.format(n)))
            raw_input("Form the indicated hand shape. Press Enter when ready.")
            hub.run_once(3000, listener)
            confirm = raw_input("Enter to save or any other input to deny.")
            if confirm == '':
                print("Saved.")
                trial_data.append(copy(listener.store_data).deepcopy())
                fing_curv.append([[int(x) for x in list('{0:05b}'.format(n))]
                                 for datum in listener.store_data])
                listener.store_data = []
                if len(listener.store_data) == 0:
                    print "Run, cleared, and flushed!"
                else:
                    raise RuntimeError("store_data (len {0}) not flushed!"
                                       .format(len(listener.store_data)))
            else:
                print("Data was not saved.")
    finally:
        hub.stop(True)
        hub.shutdown()
        dump(trial_data, fing_curv)


if __name__ == '__main__':
    main()
