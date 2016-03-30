# gesture_classifier_chords
from gesture_classifier_5 import nur_net
import pickle
import argparse
import os
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='Try machine learning on Myo data file')
    parser.add_argument('filepath', type=str, default='',
                        help='filepath of .pkl file to be analyzed')
    parser.add_argument('-hl', '--hidden', type=int, default=2,
                        help='number of hidden layers to use in the model')
    parser.add_argument('-e', '--epochs', type=int, default=30,
                        help='number of training epochs to run')
    args = parser.parse_args()
    return

if __name__ == "__main__":
    main()
