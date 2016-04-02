# gesture_classifier_chords
from gesture_classifier_5 import nur_net
from keras.utils import np_utils
import pickle
import argparse
import os
import numpy as np

# fix for python 2->3
try:
    input = raw_input
except NameError:
    pass

def rect_ave(np_arr, window_size=None):
    if len(np_arr.shape) > 1:
        raise RuntimeError("Shape {0} is not accepted, feed me a 1xN array")
    else:
        x = np.absolute(np_arr)
        if window_size is None:
            window = len(x)/20 if len(x)/20 > 5 else 5
        else:
            window = window_size
        return np.convolve(x, np.ones((window,))/window, 'same')


class category(object):
    uniques = []

    def __init__(self, string_array):
        if isinstance(string_array[0], list):
            string_array = self.iterFlatten(string_array)
        self.uniques = list(set(string_array))

    def __getitem__(self, index):
        if isinstance(index, str):
            if index in self.uniques:
                return self.uniques.index(index)
            else:
                raise IndexError("{0} is not categorized here ({1}).".format(index, self.uniques))
        elif isinstance(index, int):
            if index < len(self.uniques):
                return self.uniques[index]
            else:
                raise IndexError("{0} is longer than the the length({1}) of this array.".format(index, len(self.uniques)))
        else:
            raise IndexError("{0} is neither a String nor an Int. Please check your data inputs")

    def to_categorical(self, np_array):
        # currently stored as strings
        int_array = [self[string] for string in np_array]
        return np_utils.to_categorical(int_array)

    def from_categorical(self, np_array):
        guess = np.argmax(np_array)
        return self[guess]

    def iterFlatten(self, root, level=None):
        if level and level == 0:
            yield root
        elif isinstance(root, (list, tuple)):
            if level:
                level = level-1
            for element in root:
                for e in self.iterFlatten(element, level):
                    yield e
        else:
            yield root


def main():
    # standard - argparser for arguments and load pickle file
    parser = argparse.ArgumentParser(description='Try machine learning on Myo data file')
    parser.add_argument('filepath', type=str, default='',
                        help='filepath of .pkl file to be analyzed')
    parser.add_argument('-hl', '--hidden', type=int, default=2,
                        help='number of hidden layers to use in the model')
    parser.add_argument('-e', '--epochs', type=int, default=30,
                        help='number of training epochs to run')
    parser.add_argument('-b', '--batch', type=int, default=None,
                        help='size of mini-batches for each epoch')
    parser.add_argument('-s', '--split', type=float, default=0.25,
                        help='data split-off to be used as test data')
    parser.add_argument('-w', '--window', type=int, default=30,
                        help='size of moving average window on (100 Hz to 200 Hz expected sampling rate)')

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
                    fpaths.append(os.path.join(args.filepath, filenames))
        except:
            raise RuntimeError('No file in current directory available for analysis.')
    elif os.path.isdir(args.filepath):
        try:
            f = []
            for (dirpath, dirnames, filenames) in os.walk(args.filepath):
                f.extend(filenames)
                break
            for file in f:
                if ".pkl" in file:
                    fpaths.append(os.path.join(args.filepath, file))
        except:
            raise RuntimeError('No file in {0} available for analysis.'.format(args.filepath))
    elif os.path.isfile(args.filepath):
        fpaths.append(args.filepath)

    # build the neural net and train against the first set of data
    with open(fpaths[0], 'r') as data_file:
        data = pickle.load(data_file)
    catter = category(data["labels"])
    myo_net = nur_net(args.hidden, len(catter.uniques))
    for tri_ind in range(len(data['data'])):
        for chan_ind in range(len(data['data'][tri_ind])):
            data['data'][tri_ind][chan_ind] = rect_ave(np.array(data['data'][tri_ind][chan_ind]), window_size=args.window)
    x = np.concatenate(data['data'], 1).T
    y = catter.to_categorical(np.concatenate(data['labels'], 0))

    # overall_data to test against through iterations
    overall_data = x
    overall_results = y

    # load all the other data
    for file in fpaths[1:]:
        with open(file, 'r') as data_file:
            data = pickle.load(data_file)
        for tri_ind in range(len(data['data'])):
            for chan_ind in range(len(data['data'][tri_ind])):
                data['data'][tri_ind][chan_ind] = rect_ave(np.array(data['data'][tri_ind][chan_ind]), window_size=args.window)
        x = np.concatenate(data['data'], 1).T
        y = catter.to_categorical(np.concatenate(data['labels'], 0))
        overall_data = np.concatenate([overall_data, x])
        overall_results = np.concatenate([overall_results, y])

    print(len(overall_data))
    split_index = int(args.split*len(overall_data))
    if args.batch:
        myo_net.train(overall_data[:split_index], overall_results[:split_index], eps=args.epochs, batch_size=args.batch)
    else:
        myo_net.train(overall_data[:split_index], overall_results[:split_index], eps=args.epochs)
    [loss, acc] = myo_net.accuracy(overall_data, overall_results)

    print("loss = {0}".format(loss))
    print("accuracy = {0}".format(acc))

    name = input("If you'd like to save this run, please enter a savefile name now: ")
    if name:
        # save weights
        myo_net.save(name)
        print("saved!")
        # save configuration
        # save accuracy and loss

if __name__ == "__main__":
    main()
