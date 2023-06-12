#!/usr/bin/env python3
import pandas as pd
from sklearn.tree import DecisionTreeClassifier as Tree
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.model_selection import StratifiedKFold

#get only plaintext data 
df = pd.read_csv('features.csv')
cond1 = df['class'] == 0
cond2 = df['algorithm'] == 'aes'
df = df[cond1 & cond2]
y = df['filetype']
X = df.drop(['algorithm', 'filetype', 'class'], axis=1)

tree = Tree()
skf = StratifiedKFold()
yp = cross_val_predict(tree, X, y, cv=skf)
print(accuracy_score(y,yp))