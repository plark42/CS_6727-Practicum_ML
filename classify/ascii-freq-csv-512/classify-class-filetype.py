#!/usr/bin/env python3
#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier as Tree
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.model_selection import StratifiedKFold

df = pd.read_csv('features.csv')
results = []

for filetype in np.unique(df['filetype']):
    cond1 = df['filetype'] == filetype
    cond2 = df['class'] == 1
    data = df[cond1 & cond2]
    
    cond1 = df['class'] == 0
    cond2 = df['algorithm'] == 'aes'
    cond3 = df['filetype'] == filetype
    plain = df[cond1 & cond2 & cond3]
    plain['algorithm'] = 'plaintext'
    data = pd.concat([data, plain])
    
    X = data.drop(['class', 'algorithm', 'filetype'], axis=1)
    y = data['class']
    tree = Tree()
    skf = StratifiedKFold()

    yp = cross_val_predict(tree, X, y, cv=skf)
    acc = accuracy_score(y,yp)*100
    pre = precision_score(y, yp)*100
    rec = recall_score(y,yp)*100
    print(filetype, acc, pre, rec)
    
    results.append([filetype, acc, pre, rec])

results = pd.DataFrame(results, columns=['filetype', 'accuracy', 'precision', 'recall'])
results.to_csv('tree-results.csv', index=False)
results.plot.bar(x='filetype')
plt.legend(loc='lower right')
plt.ylabel('percentage (%)')
plt.title('5-fold X-val classification results (tree)')