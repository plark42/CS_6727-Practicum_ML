#!/usr/bin/env python3
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd

df = pd.read_csv('features.csv')
pd.set_option('mode.use_inf_as_na', True)
df.fillna(0, inplace=True)

# df.loc[df['class']==1,'filetype'] = 'encrypted'
X = df.drop(['filename', 'algorithm', 'filetype', 'class'], axis=1)
X['mime'] = LabelEncoder().fit_transform(X['mime'])
y = df['class']

random_forest = RandomForestClassifier()
cv = KFold(n_splits=5, shuffle=True, random_state=42)
yp = cross_val_predict(random_forest, X, y, cv=cv, n_jobs=10)
acc = 100 * accuracy_score(y,yp)
pre = 100 * precision_score(y,yp)
rec = 100 * recall_score(y,yp)
index = y != yp
print(acc, pre, rec)
print(df['filename'][index])

