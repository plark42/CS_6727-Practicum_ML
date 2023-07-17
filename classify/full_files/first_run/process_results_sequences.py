#!/usr/bin/env python3
import glob
from collections import Counter
from sklearn.metrics import accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt

seq_lens = list(range(1,50))
acc = {}
pre = {}
rec = {}

for seq_len in seq_lens:
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
                
                preds_str = ''.join([str(p) for p in preds])
                seq = '1' * seq_len
                
                if seq in preds_str:
                    yp.append(1)
                else:
                    yp.append(0)
                
                
    acc[seq_len] = 100 * accuracy_score(y,yp)
    pre[seq_len] = 100 * precision_score(y,yp)
    rec[seq_len] = 100 * recall_score(y,yp)

plt.figure()
plt.title('classification based on number of consecutive encrypted blocks')
plt.plot(acc.keys(), acc.values())
plt.plot(pre.keys(), pre.values())
plt.plot(rec.keys(), rec.values())
plt.xlabel('number of sequential "encrypted" blocks')
plt.ylabel('percentage (%)')
plt.legend(['accuracy', 'precision', 'recall'])
plt.show()
