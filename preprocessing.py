import pickle
import numpy as np
import argparse
import os


def load_pkl(filepath):
    with open(filepath, 'r') as data_file:
        raw_data = pickle.load(data_file)
    return raw_data


def reshape(raw_data):
    data = {'data': [], 'labels': []}
    data['data'] = list(np.array([dp for trial in raw_data['data'] for dp in trial]).T)
    data['labels'] = list(np.array([lp for trial in raw_data['labels'] for lp in trial]).T)
    return data


def rect_ave(raw_data):
    data = {'labels': raw_data['labels'], 'data': []}
    for channel in raw_data['data']:
        x = np.absolute(channel)
        data['data'].append(np.convolve(x, np.ones((30,))/30, 'same'))
    return data

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

    raw_data = load_pkl(args.filepath)
    raw_data = reshape(raw_data)
    data = rect_ave(raw_data)

    with open('{0}.fix'.format(args.filepath), 'w') as new_data:
        pickle.dump(data, new_data)
