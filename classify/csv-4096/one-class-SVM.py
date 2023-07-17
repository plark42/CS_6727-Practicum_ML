#!/usr/bin/env python3
from sklearn.svm import OneClassSVM
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle

df = pd.read_csv('features.csv')
pd.set_option('mode.use_inf_as_na', True)
df.fillna(0, inplace=True)

X = df.drop(['filetype', 'algorithm', 'class'], axis=1)
y = df['class']

#X1 = X[y==1]
# ocsvm = OneClassSVM(gamma='auto')
# ocsvm.fit(X1)
with open('ocsvm.pkl', 'rb') as f:
    ocsvm = pickle.load(f)

kf = KFold(n_splits=5)
y_true = []
y_pred = []
for train, test in kf.split(X,y):
    X_train = X.iloc[train]
    y_train = y.iloc[train]
    X_test = X.iloc[test]
    y_test = y.iloc[test]
    
    #build one-class SVM on training 
    X1 = X_train[y_train==1]
    ocsvm = OneClassSVM()
    ocsvm.fit(X1)
    X_train['OCSVM'] = ocsvm.predict(X_train)
    X_test['OCSVM'] = ocsvm.predict(X_test)
    
    random_forest = RandomForestClassifier()
    random_forest.fit(X_train, y_train)
    yp = random_forest.predict(X_test)
    y_true.append(y_test)
    y_pred.append(yp)
    
    
    