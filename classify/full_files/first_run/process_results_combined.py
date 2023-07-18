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
                pln = int(words[2].split('pln=')[1])
                enc = int(words[3].split('enc=')[1])
                
                if 'plaintext' in filename:
                    y.append(0)
                else:
                    y.append(1)
                                 
                enc_ratio = enc / (enc + pln)
                preds = ''.join(preds.split(','))

                len_max_seq = int(len(preds) * 0.25)
                s = '1' * len_max_seq
                
                if enc_ratio > ratio and s in preds:
                    yp.append(1)
                else:
                    yp.append(0)
                
                
    acc[ratio] = 100 * accuracy_score(y,yp)
    pre[ratio] = 100 * precision_score(y,yp)
    rec[ratio] = 100 * recall_score(y,yp)

plt.figure()
plt.title('classification based on combination')
plt.plot(acc.keys(), acc.values())
plt.plot(pre.keys(), pre.values())
plt.plot(rec.keys(), rec.values())
plt.xlabel('ratio of "encrypted" blocks')
plt.ylabel('percentage (%)')
plt.legend(['accuracy', 'precision', 'recall'])
plt.show()
