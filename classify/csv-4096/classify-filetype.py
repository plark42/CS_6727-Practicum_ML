#!/usr/bin/env python3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd

df = pd.read_csv('features.csv')
pd.set_option('mode.use_inf_as_na', True)
df.fillna(0, inplace=True)

df.loc[df['class']==1,'filetype'] = 'encrypted'
X = df.drop(['algorithm', 'filetype', 'class'], axis=1)
y = df['filetype']

random_forest = RandomForestClassifier()
yp = cross_val_predict(random_forest, X, y)

acc = 100 * accuracy_score(y,yp)
pre = 100 * precision_score(y,yp, average='macro')
rec = 100 * recall_score(y,yp,average='macro')
print(acc, pre, rec)

