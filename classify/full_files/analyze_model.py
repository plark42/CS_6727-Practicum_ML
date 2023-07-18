#!/usr/bin/env python3
from feature_extraction import get_features 
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd
import sys
import pickle
from collections import Counter

mimes = ['application/gzip', 'application/octet-stream', 'application/pdf', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',     'application/x-dosexec', 'application/x-executable', 'application/x-mach-binary', 'application/x-mach-binary\ntmp (for architecture x86_64):\t', 'application/zip', 'audio/mpeg', 'audio/x-wav', 'image/gif', 'image/jpeg', 'image/png', 'text/html', 'text/plain', 'video/mp4', 'video/quicktime']

labelEncoder = LabelEncoder()
labelEncoder.fit(mimes)

pd.set_option('mode.use_inf_as_na', True)
pd.options.mode.chained_assignment = None

df = pd.read_csv('features.csv')
df.fillna(0, inplace=True)

df['mime'] = labelEncoder.transform(df['mime'])

y  = []
yp = []
testfiles = []

for i in range(1,6):
    print('analyzing %d of 5' % i)
    modelname = 'random_forest_%d.pkl' % i
    f = open(modelname, 'rb')
    random_forest = pickle.load(f)
    f.close()

    testfile = 'test_%d.txt' % i
    f = open(testfile, 'r')
    lines = f.readlines()
    f.close()
    
    for line in lines:
        pln = False
        if 'plaintext' in line:
            pln = True
        filename = line.strip().split('/')[-1]
        testfiles.append(filename)

        if pln == True:
            index = (df['filename'] == filename) & (df['algorithm'] == 'aes')
        else:
            index = df['filename'] == filename

        X = df[index]
        X.drop(['class', 'algorithm', 'filename', 'filetype'], axis=1, inplace=True)
        pred = random_forest.predict(X)
    
        if 1 in df['class'][index].values:
            c = 1
        else:
            c = 0

        if 1 in pred:
            pred = 1
        else:
            pred = 0

        y.append(c)
        yp.append(pred)
        if c != pred:
            print(filename)

acc = 100 * accuracy_score(y,yp)
pre = 100 * precision_score(y,yp)
rec = 100 * recall_score(y,yp)
print(acc, pre, rec)
