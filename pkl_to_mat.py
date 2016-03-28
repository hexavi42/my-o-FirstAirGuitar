# pkl to matlab converter
# if run, makes matlab versions of all pkl files in directory
import pickle
import scipy.io
import os

def convert_to_mat(pkl_fname):
    with open(pkl_fname, 'rb') as data_file:
        data = pickle.load(data_file)
    scipy.io.savemat('./{0}.mat'.format(pkl_fname), mdict={'data': data['data'], 'labels': data['labels']})

def main():
    print("converting all .pkl files in {0}".format(os.getcwd()))
    for file in os.listdir("."):
        if file.endswith(".pkl"):
            text = open(file, 'rb').read().replace('\r\n', '\n')
            open("unix_{0}".format(file), 'wb').write(text)
            convert_to_mat("unix_{0}".format(file))

if __name__ == "__main__":
    main()