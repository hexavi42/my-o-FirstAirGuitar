# pkl to matlab converter
# if run, makes matlab versions of all pkl files in directory
import pickle
import scipy.io
import os

cwd = os.path.dirname(os.path.realpath(__file__))


def convert_to_mat(pkl_fname):
    with open(pkl_fname, 'rb') as data_file:
        data = pickle.load(data_file)
    if not os.path.isdir("{0}/{1}".format(cwd, "mat")):
            os.makedirs("{0}/{1}".format(cwd, "mat"))
    scipy.io.savemat('./mat/{0}.mat'.format(pkl_fname), mdict={'data': data['data'], 'labels': data['labels']})


def main():
    print("converting all .pkl files in {0}".format(os.getcwd()))
    # temporary storage for unix versions of file - might be from windows
    if not os.path.isdir("{0}/{1}".format(cwd, "tmp_unix")):
            os.makedirs("{0}/{1}".format(cwd, "tmp_unix"))
    for file in os.listdir("."):
        if file.endswith(".pkl"):
            text = open(file, 'rb').read().replace('\r\n', '\n')
            open("tmp_unix/unix_{0}".format(file), 'wb').write(text)
            convert_to_mat("tmp_unix/unix_{0}".format(file))

if __name__ == "__main__":
    main()