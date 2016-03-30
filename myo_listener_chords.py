import myo as libmyo
import copy
import re
from myo_listener_freestyle import EmgListen, lblDataDump


def scrape_chords(tab_file):
    chords = []
    fingerings = {}
    chord_arr = set(['a', 'b', 'c', 'd', 'e', 'f', 'g',
                     'A', 'B', 'C', 'D', 'E', 'F', 'G',
                     'm', 's', 'u', '9', '7', '4', '#',
                     '/', '\\', ' ', '\t', '\n'])
    fing_syn = re.compile("([A-z0-9#/\\\]{1,9})[ \t]*\(?([ 0-9x]{6,18})\)?")
    with open(tab_file, 'r') as tab:
        for line in tab.readlines():
            # check if this is a line that contains chord names
            if set(list(line)) <= chord_arr:
                chordLine = re.findall("\S*", line)
                for chord in chordLine:
                    # remove blank results
                    if chord != '':
                        chords.append(chord)
            # TODO: consider scraping chord fingerings from web as well
            elif fing_syn.match(line):
                match_obj = fing_syn.match(line)
                fingerings[match_obj.groups()[0]] = match_obj.groups()[1]
    return list(set(chords)), fingerings


def main(chords=['G', "C", "Em", "D", "No chord - relax your hand"], fingerings={}):
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
            print("Run, cleared, and flushed!")
        else:
            raise RuntimeError("store_data cache not flushed!")

        print("""Bend your fingers to form the indicated chord\n
        as you know the fretting - if you don't know the chord,\n
        use the first result from Googling the chord name.\n
        "E.g. Em7 (022033):\n""")

        # record EMG data per chord
        for chord in chords:
            while True:
                if chord in fingerings:
                    print("{0} ({1})".format(chord, fingerings[chord]))
                else:
                    print(chord)
                raw_input("Form the indicated chord. Press Enter when ready.")
                hub.run_once(3000, listener)
                confirm = raw_input("Enter to save or any other input to deny.")
                if confirm == '':
                    print("Saved.")
                    trial_data.append(copy.deepcopy(listener.store_data))
                    fing_curv.append([chord for datum in listener.store_data])
                    listener.store_data = []  # clear stored data between runs
                    if len(listener.store_data) != 0:  # make sure it's cleared
                        raise RuntimeError("store_data (len {0}) not flushed!"
                                           .format(len(listener.store_data)))
                    break
                else:
                    print("Data was not saved.")
    finally:
        hub.stop(True)
        hub.shutdown()
        lblDataDump(trial_data, fing_curv)


if __name__ == '__main__':
    #chords, fingerings = scrape_chords('wonderwall_tab.txt')
    main()
