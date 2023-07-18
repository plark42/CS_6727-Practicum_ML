#!/usr/bin/env python3
from feature_extraction import get_features
from sklearn.preprocessing import LabelEncoder 
import subprocess
import sys, pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

DATAPATH = '/Users/fac_rubin/Documents/GeorgiaTech/CS_6727-Practicum/data/'

mimes = ['application/gzip', 'application/octet-stream', 'application/pdf', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/x-dosexec', 'application/x-executable', 'application/x-mach-binary', 'application/x-mach-binary\ntmp (for architecture x86_64):\t', 'application/zip', 'audio/mpeg', 'audio/x-wav', 'image/gif', 'image/jpeg', 'image/png', 'text/html', 'text/plain', 'video/mp4', 'video/quicktime']

columns = ['kurtosis', 'entropy', 'stdev', 'pi', 'mse',\
         'chi', 'p', 'autocorr', 'mean', 'bigrams', 'ics',\
         'hmean', 'skew', 'mime', 'class']

pd.set_option('mode.use_inf_as_na', True)

if len(sys.argv) != 3:
    print('usage: ./train_model.py training.txt model.pkl')
    exit(1)

training_data = pd.DataFrame(columns=columns)

labelEncoder = LabelEncoder()
labelEncoder.fit(mimes)

df = pd.read_csv('features.csv')
pd.set_option('mode.use_inf_as_na', True)
df.fillna(0, inplace=True)

with open(sys.argv[1], 'r') as file:
    lines = file.readlines()

    n = 0
    for line in lines:
        n += 1
        filename = line.strip().split('/')[-1]
        print('processing %d of %d' % (n, len(lines)))
        if 'plaintext' in line:
            i = (df['filename'] == filename) & (df['algorithm'] == 'aes')
        else: 
            i = df['filename'] == filename

        features = df[columns][i]
        features['mime'] = labelEncoder.transform(features['mime'])        
        training_data = pd.concat([training_data, features])

print('training random forest..')
random_forest = RandomForestClassifier()
X = training_data.drop('class', axis=1)
X.fillna(0, inplace=True)
y = training_data['class'].astype('int')
random_forest.fit(X,y)

print('writing model to file')
with open(sys.argv[2], 'wb') as f:
    pickle.dump(random_forest, f)

print('done')
