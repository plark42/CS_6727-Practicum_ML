#!/usr/bin/env python3
from feature_extraction import get_features 
import sys, pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

DATAPATH = '/Users/fac_rubin/Documents/GeorgiaTech/CS_6727-Practicum/data/'

pd.set_option('mode.use_inf_as_na', True)
if len(sys.argv) != 3:
    print('usage: ./count_block_predictions.py training.txt model.pkl')
    exit(1)

columns = ['kurtosis', 'entropy', 'stdev', 'pi', 'mse',\
         'chi', 'p', 'autocorr', 'mean', 'bigrams', 'ics', 'hmean', 'skew', 'class']
training_data = pd.DataFrame(columns=columns)

with open(sys.argv[1], 'r') as file:
    for line in file:
        infile = DATAPATH + line.strip()
        print('processing', infile)
        datafile = open(infile, 'rb')
        _bytes = datafile.read()
        datafile.close()

        for i in range(0, len(_bytes), 4096):
            data = _bytes[i:i+4096]
            if len(data) < 4096:
                diff = 4096 - len(data)
                data += bytes(diff) 

            features = get_features(data)
            if 'plaintext' in infile:
                features['class'] = 0
            else:
                features['class'] = 1
            training_data = pd.concat([training_data, features])

random_forest = RandomForestClassifier()
X = training_data.drop('class', axis=1)
X.fillna(0, inplace=True)
y = training_data['class'].astype('int')
random_forest.fit(X,y)

with open(sys.argv[2], 'wb') as f:
    pickle.dump(random_forest, f)

