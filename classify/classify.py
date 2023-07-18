#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier as MLP
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score
import sys
from collections import Counter

if len(sys.argv) != 3:
    print('usage: ./classify.py file.csv fig.png')
    exit(1)

file = sys.argv[1]
fig = sys.argv[2]

df = pd.read_csv(file)
X = df.drop('class', axis=1)
y = df['class']

# convert to byte frequency
data = []
totals = Counter(dict([(x,0) for x in range(256)]))
for row in X.values:
    counts = Counter(row)
    for c in counts:
        totals.update({c: counts[c]})
    totals = dict(sorted(totals.items()))
    data.append(list(totals.values()))    
X = pd.DataFrame(data)

#normalize data 
X = X / 512.0

mlp = MLP()
yp = cross_val_predict(mlp, X, y)
acc = accuracy_score(y,yp)*100
pre = precision_score(y,yp)*100
rec = recall_score(y,yp)*100
file = file.strip('csv/').strip('.').replace('.',' ')
print(file, acc, pre, rec)
rects = plt.bar([1,2,3], [acc,pre,rec], color=['red', 'green', 'blue'])
plt.title('MLP Cross-Validation Results: ' + file)
plt.xticks([1,2,3], ['Accuracy', 'Precision', 'Recall'])
plt.xlabel('metric')
plt.ylabel('percentage (%)')
plt.yticks([0,20,40,60,80,100])
for r in rects:
    x = r.get_x()
    y = r.get_height()
    w = r.get_width()
    plt.text(x + w/2., 0.9*y, '%.2f%%' % y, ha='center')
plt.savefig(fig)
