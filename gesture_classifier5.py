from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import pickle


class nur_net(object):
    model = None

    def __init__(self):
        model = Sequential()
        # Dense(64) is a fully-connected layer with 64 hidden units.
        # in the first layer, you must specify the expected input data shape:
        # here, 20-dimensional vectors.
        model.add(Dense(32, input_dim=8, init='uniform'))
        model.add(Activation('tanh'))
        model.add(Dropout(0.5))
        model.add(Dense(32, init='uniform'))
        model.add(Activation('tanh'))
        model.add(Dropout(0.5))
        model.add(Dense(5, init='uniform'))
        model.add(Activation('softmax'))

        sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd)
        self.model = model

    def train(self, x, y):
        self.model.fit(x, y, nb_epoch=30, batch_size=1000, show_accuracy=True)

    def accuracy(self, x, y):
        return self.model.evaluate(x, y, batch_size=1000)


def main():
    samples = pickle.load(open('myo_data.pkl', 'r'))
    myo_net = nur_net()
    myo_net.train(samples['data'], samples['labels'])

if __name__ == "__main__":
    main()
