#!/usr/bin/env python3
import warnings
warnings.simplefilter(action='ignore', category=Warning)

import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold
from sklearn.decomposition import PCA
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.model_selection import cross_val_predict
from sklearn.neural_network import MLPClassifier

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
    
    Xt = []
    for x in X.values:
        x = np.array(x).reshape((64,64))
        xt = PCA(2).fit_transform(x)
        xt = xt.flatten()
        Xt.append(xt)
        
    Xt = np.array(Xt)
    yp = cross_val_predict(MLPClassifier(1024), Xt, y, cv=5)
    print(accuracy_score(yp, y))
    break
