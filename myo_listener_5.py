import myo as libmyo
import copy
from myo_listener_freestyle import EmgListen, lblDataDump


def main():
    fing_curv = []
    trial_data = []
    libmyo.init()
    listener = EmgListen()
    hub = libmyo.Hub()
    try:
        # warm up (first run seems to have shorter data length, idk why)
        hub.run_once(1000, listener)
        listener.store_data = []  # clear stored data between runs
        if len(listener.store_data) == 0:  # make sure it's cleared
            print "Run, cleared, and flushed!"
        else:
            raise RuntimeError("store_data cache not flushed!")

        print("""Bend your fingers as indicated by the printed array\n
        where 1 indicates bent and 0 indicates unbent,\n
        "starting with your thumb and ending with your pinky.\n
        "E.g. index finger bent, the rest unbent would be '01000':\n""")

        # 2^5 possible configurations for five fingers, on/off
        for n in range(2**5):
            print(list('{0:05b}'.format(n)))
            raw_input("Form the indicated hand shape. Press Enter when ready.")
            hub.run_once(3000, listener)
            confirm = raw_input("Enter to save or any other input to deny.")
            if confirm == '':
                print("Saved.")
                trial_data.append(copy(listener.store_data).deepcopy())
                fing_curv.append([[int(x) for x in list('{0:05b}'.format(n))]
                                 for datum in listener.store_data])
                listener.store_data = []  # clear stored data between runs
                if len(listener.store_data) == 0:  # make sure it's cleared
                    print "Run, cleared, and flushed!"
                else:
                    raise RuntimeError("store_data (len {0}) not flushed!"
                                       .format(len(listener.store_data)))
            else:
                print("Data was not saved.")
    finally:
        hub.stop(True)
        hub.shutdown()
        lblDataDump(trial_data, fing_curv)


if __name__ == '__main__':
    main()
