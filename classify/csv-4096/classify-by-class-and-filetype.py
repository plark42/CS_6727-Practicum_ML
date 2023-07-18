#!/usr/bin/env python3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd

df = pd.read_csv('features.csv')
pd.set_option('mode.use_inf_as_na', True)
df.fillna(0, inplace=True)

df.loc[df['class']==1,'filetype'] = 'encrypted'
X = df.drop(['algorithm', 'filetype', 'class'], axis=1)

# random_forest = RandomForestClassifier()
# yp = cross_val_predict(random_forest, X, y)

# acc = 100 * accuracy_score(y,yp)
# pre = 100 * precision_score(y,yp, average='macro')
# rec = 100 * recall_score(y,yp,average='macro')
# print(acc, pre, rec)

y_class = df['class']
y_filetype = df['filetype']

kf = KFold(n_splits=5, shuffle=True)
y_true = []
y_pred = []

for train, test in kf.split(X,y_class):
    X_train = X.iloc[train]
    y_train_class = y_class.iloc[train]
    y_train_filetype = y_filetype.iloc[train]

    X_test = X.iloc[test]
    y_test_class = y_class.iloc[test]
    y_test_filetype = y_filetype.iloc[test]

    random_forest = RandomForestClassifier()

    random_forest.fit(X_train, y_train_class)
    yp_class = random_forest.predict(X_test)
    
    random_forest.fit(X_train, y_train_filetype)
    yp_filetype = random_forest.predict(X_test)

    yp = []
    for i in range(len(yp_class)):
        if yp_class[i] == 1 and yp_filetype[i] == 'encrypted':
            yp.append(1)
        else:
            yp.append(0)
            
    y_true.append(y_test_class)
    y_pred.append(yp)
    
    print(accuracy_score(y_test_class, yp))
        
    
    
    
    