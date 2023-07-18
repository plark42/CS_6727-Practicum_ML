#!/usr/bin/env python3
import warnings
warnings.simplefilter(action='ignore', category=Warning)

import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score, mean_squared_error
from sklearn.model_selection import cross_val_predict

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
    y = df['class'].values
    
    norm = np.linspace(start=0, stop=256, num=4096, dtype='int')

    i = 0    
    for x in X.values:
        x = sorted(x)
        mse = mean_squared_error(x, norm)
        print(mse, y[i])
        i += 1