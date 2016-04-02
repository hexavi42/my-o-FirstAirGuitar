# gesture_classifier_chords
from gesture_classifier_5 import nur_net
import pickle
import argparse
import os
import numpy as np

def main():
    # standard - argparser for arguments and load pickle file
    parser = argparse.ArgumentParser(description='Try machine learning on Myo data file')
    parser.add_argument('filepath', type=str, default='',
                        help='filepath of .pkl file to be analyzed')
    parser.add_argument('-hl', '--hidden', type=int, default=2,
                        help='number of hidden layers to use in the model')
    parser.add_argument('-e', '--epochs', type=int, default=30,
                        help='number of training epochs to run')
    # Ryan ran 50 separate trials, so we're configuring this to run for multiple files
    args = parser.parse_args()
    fpaths = []
    if not args.filepath:
        try:
            f = []
            for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
                f.extend(filenames)
                break
            for file in f:
                if ".pkl" in file:
                    fpaths.append(file)
        except:
            raise RuntimeError('No file in current directory available for analysis.')
    elif os.isdir(args.filepath):
        try:
            f = []
            for (dirpath, dirnames, filenames) in os.walk(args.filepath):
                f.extend(filenames)
                break
            for file in f:
                if ".pkl" in file:
                    fpaths.append(file)
        except:
            raise RuntimeError('No file in {0} available for analysis.'.format(args.filepath))
    elif os.isfile(args.filepath):
        fpaths.append(args.filepath)

    samples = pickle.load(open(args.filepath, 'r'))
    myo_net = nur_net(args.hidden)

if __name__ == "__main__":
    main()
