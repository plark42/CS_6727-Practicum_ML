#!/usr/bin/env python3
import glob
from collections import Counter
from sklearn.metrics import accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt

ratios = [(x)/100 for x in range(100)]
#ratios.append(0.99)
acc = {}
pre = {}
rec = {}

for ratio in ratios:
    y = []
    yp = []
    for result_file in sorted(glob.glob('results_*.txt')):
        with open(result_file, 'r') as f:
            for line in f:
                line = line.strip()
                words = line.split('; ')
                filename = words[0]
                preds = words[1]
                pln = words[2]
                enc = words[3]
                
                if 'plaintext' in filename:
                    y.append(0)
                else:
                    y.append(1)
                
                preds = preds.split(',')
                preds = [int(x) for x in preds]
                counts = Counter(preds)
                
                enc_ratio = counts[1] / (counts[0] + counts[1])
                
                if enc_ratio > ratio:
                    yp.append(1)
                else:
                    yp.append(0)
                
                
    acc[ratio] = 100 * accuracy_score(y,yp)
    pre[ratio] = 100 * precision_score(y,yp)
    rec[ratio] = 100 * recall_score(y,yp)

plt.figure()
plt.title('classification based on ratio of encrypted blocks')
plt.plot(acc.keys(), acc.values())
plt.plot(pre.keys(), pre.values())
plt.plot(rec.keys(), rec.values())
plt.xlabel('ratio of "encrypted" blocks')
plt.ylabel('percentage (%)')
plt.legend(['accuracy', 'precision', 'recall'])
plt.show()
