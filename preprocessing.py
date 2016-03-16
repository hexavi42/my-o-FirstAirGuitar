import pickle
import numpy as np
import argparse
import os
import copy


def load_pkl(filepath):
    with open(filepath, 'r') as data_file:
        data = pickle.load(data_file)
    return data


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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rectify and convolve Myo data, storing it in a new object.')
    parser.add_argument('filepath', type=str, default='',
                        help='filepath of .pkl file to be converted')
    args = parser.parse_args()
    if not args.filepath:
        try:
            f = []
            for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
                f.extend(filenames)
                break
            for file in f:
                if ".pkl" in file:
                    args.filepath = file
                    break
        except:
            raise RuntimeError('No file in current directory available for conversion.')

    data = load_pkl(args.filepath)
    for trial in data['data']:
        for channel in data:
            channel = rect_ave(channel)

    with open('{0}.proc'.format(args.filepath), 'w') as new_data:
        pickle.dump(data, new_data)
