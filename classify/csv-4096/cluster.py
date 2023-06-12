#!/usr/bin/env python3
import pandas as pd
from sklearn.cluster import  KMeans
from collections import Counter
import matplotlib.pyplot as plt
import random
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('features.csv')
pd.set_option('mode.use_inf_as_na', True)
df.fillna(0, inplace=True)

y = df['class']

X0 = df[y==0]
X1 = df[y==1]

# mse = []
# for k in range(1,21):
#     kmeans = KMeans(k)
#     kmeans.fit(encr)
#     print(k, kmeans.inertia_)
#     mse.append(kmeans.inertia_)
    
# plt.plot(list(range(1,21)), mse)

#cluster encrypted data into 5 groups 
# kmeans = KMeans(5).fit(X1)
# clusters = kmeans.labels_
counts = Counter(X1['filetype'])
weights = [counts[ft] / len(X1) for ft in X1['filetype']]
X1 = X1.sample(n=len(X0), weights=weights)

#create data 
X = X0.append(X1)
X.fillna(0,inplace=True)
X = X.drop(['class', 'algorithm', 'filetype'], axis=1)
y = [0 if i < (len(X)/2) else 1 for i in range(len(X))]

yp = cross_val_predict(RandomForestClassifier(), X, y, cv=5)
acc = accuracy_score(y,yp)*100
pre = precision_score(y, yp)*100
rec = recall_score(y,yp)*100
print(acc, pre, rec)
