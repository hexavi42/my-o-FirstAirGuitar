import pickle
import numpy as np
import argparse
import os
import copy


def load_pkl(filepath):
    with open(filepath, 'r') as data_file:
        data = pickle.load(data_file)
    return data


def process(raw_data):
    data = {'labels': [], 'data': []}
    all_trial_data = [[] for channels in raw_data['data'][0][0]]
    for trial in raw_data['data']:
        for channel_no in range(len(np.array(trial).T)):
            all_trial_data[channel_no].extend(rect_ave(np.array(trial).T[channel_no]))
    data['data'] = all_trial_data
    data['labels'] = list(np.array([lp for trial in raw_data['labels'] for lp in trial]).T)
    print(len(data['data']))
    print(len(data['data'][0]))
    return data


def rect_ave(np_arr):
    x = np.absolute(np_arr)
    window = len(x)/10 if len(x)/10 > 2 else 2
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
    data = process(data)

    with open('{0}.proc'.format(args.filepath), 'w') as new_data:
        pickle.dump(data, new_data)
