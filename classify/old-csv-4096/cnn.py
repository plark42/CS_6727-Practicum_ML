#!/usr/bin/env python3
import warnings
warnings.simplefilter(action='ignore', category=Warning)

import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D

from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score

def CNN():
    model = Sequential()
    model.add(Conv2D(filters=64, \
                            kernel_size=(5,5), \
                            padding='valid', \
                            input_shape=(64,64,1), activation='tanh'))
    model.add(MaxPooling2D(pool_size=(3,3)))
    model.add(Conv2D(filters=64, \
            kernel_size=(5,5), \
            padding='valid', \
            activation='tanh', \
            data_format='channels_last'))
    model.add(MaxPooling2D(pool_size=(3,3)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dense(2, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

csvfiles = glob.glob('*.zip.csv')
filenum = 1
for f in csvfiles:
    algorithm = f.split('.')[0]
    filetype = f.split('.')[1]
    print(algorithm, filetype, filenum, 'of', len(csvfiles))
    filenum += 1
    
    df = pd.read_csv(f)
    print(len(df))
    
    X = df.drop('class', axis=1)
    X = X.values.reshape((len(X), 64, 64, 1))
    X = X / 255.0
    y = df['class'].values
    yc = np_utils.to_categorical(y) #convert to one-hot encoding

    kFold = StratifiedKFold(n_splits=5, shuffle=True)
    for train, test in kFold.split(X, y):
        num_classes = yc.shape[1] #get number of classes ()
        cnn = CNN()
        cnn.fit(X[train], yc[train], epochs=10, shuffle=True, validation_split=0.3, batch_size=10)
        yp = cnn.predict(X[test])
        yp = np.argmax(yp, axis=1)
        print(accuracy_score(y[test], yp))
        break

        
