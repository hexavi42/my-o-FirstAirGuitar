from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import pickle
import argparse
import os
import numpy as np


class nur_net(object):
    model = None

    def __init__(self, h_lay=2, num_outputs=5):
        model = Sequential()
        # Dense(32) is a fully-connected layer with 64 hidden units.
        # in the first layer, you must specify the expected input data shape:
        # here, 20-dimensional vectors.
        model.add(Dense(32, input_dim=8, init='uniform'))
        model.add(Activation('tanh'))
        model.add(Dropout(0.5))
        for i in range(h_lay-1):
            model.add(Dense(32, init='uniform'))
            model.add(Activation('tanh'))
            model.add(Dropout(0.5))
        model.add(Dense(num_outputs, init='uniform'))
        model.add(Activation('softmax'))

        sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd)
        self.model = model

    def train(self, x, y, eps=30, batch_sz=None):
        if batch_sz is None:
            batch_sz = len(x)/100
        self.model.fit(x, y, nb_epoch=eps, batch_size=batch_sz, show_accuracy=True)

    def loss(self, x, y):
        return self.model.evaluate(x, y, batch_size=1000)

    def accuracy(self, x, y):
        return self.model.test_on_batch(x, y, accuracy=True)

    def predict(self, x, batch_sz=128):
        return self.model.predict(x, batch_size=batch_sz, verbose=0)

    def save(self, fname):
        return self.model.save_weights(fname, overwrite=False)

    def load(self, fname):
        return self.model.load_weights(fname)


def main():
    parser = argparse.ArgumentParser(description='Try machine learning on Myo data file')
    parser.add_argument('filepath', type=str, default='',
                        help='filepath of .pkl file to be analyzed')
    parser.add_argument('-hl', '--hidden', type=int, default=2,
                        help='number of hidden layers to use in the model')
    parser.add_argument('-e', '--epochs', type=int, default=30,
                        help='number of training epochs to run')
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
            raise RuntimeError('No file in current directory available for analysis.')
    samples = pickle.load(open(args.filepath, 'r'))
    myo_net = nur_net(args.hidden)
    x_data = np.array(samples['data']).T
    y_data = np.array(samples['labels']).T
    myo_net.train(x_data, y_data, eps=args.epochs)
    [loss, acc] = myo_net.accuracy(x_data, y_data)
    acc = int(acc*100)
    save_name = "{0}_lw_h{1}_e{2}_a{3}".format(args.filepath.split('.')[0],
                                               args.hidden, args.epochs, acc)
    myo_net.save(save_name)

if __name__ == "__main__":
    main()
