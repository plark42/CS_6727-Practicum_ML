#!/usr/bin/env python3
import glob
from collections import Counter
from sklearn.metrics import accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt

pln_ratios = {}
enc_ratios = {}

pln_max_seq = {}
enc_max_seq = {}

for result_file in sorted(glob.glob('results_*.txt')):
    with open(result_file, 'r') as f:
        for line in f:
            line = line.strip()
            words = line.split('; ')
            filename = words[0]
            filetype = filename.split('/')[-2]
            
            preds = ''.join(words[1].split(','))
            
            pln = int(words[2].split('pln=')[1])
            enc = int(words[3].split('enc=')[1])
            ratio = enc / (pln + enc)
            
            if 'plaintext' in filename:
                if filetype not in pln_ratios:
                    pln_ratios[filetype] = []
                pln_ratios[filetype].append(ratio)  

                for p in range(len(preds)):
                    s = '1'*p
                    if s not in preds:
                        break
                if filetype not in pln_max_seq:
                    pln_max_seq[filetype] = []
                pln_max_seq[filetype].append(len(s)/len(preds))

            else:
                if filetype not in enc_ratios:
                    enc_ratios[filetype] = []
                enc_ratios[filetype].append(ratio)
               
                for p in range(len(preds)):
                    s = '1'*p
                    if s not in preds:
                        break
                if filetype not in enc_max_seq:
                    enc_max_seq[filetype] = []
                enc_max_seq[filetype].append(len(s)/len(preds))

plt.figure()                
plt.boxplot(pln_ratios.values())
plt.gca().set_xticklabels(pln_ratios.keys(), rotation=90)
plt.title('plaintext files')
plt.xlabel('filetype')
plt.ylabel('ratio of "encrypted" blocks')
plt.show()

plt.figure()                
plt.boxplot(enc_ratios.values())
plt.gca().set_xticklabels(enc_ratios.keys(), rotation=90)
plt.title('encrypted files')
plt.xlabel('filetype')
plt.ylabel('ratio of "encrypted" blocks')
plt.show()

plt.figure()                
plt.boxplot(pln_max_seq.values())
plt.gca().set_xticklabels(pln_max_seq.keys(), rotation=90)
plt.title('plaintext files')
plt.xlabel('filetype')
plt.ylabel('max consecutive "encrypted" blocks (% of total)')
plt.show()

plt.figure()                
plt.boxplot(enc_max_seq.values())
plt.gca().set_xticklabels(enc_max_seq.keys(), rotation=90)
plt.title('encrypted files')
plt.xlabel('filetype')
plt.ylabel('max consecutive "encrypted" blocks (% of total)')
plt.show()