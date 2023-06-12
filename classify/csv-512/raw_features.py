#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import entropy, kurtosis

df = pd.read_csv('aes.zip.csv')

X = df.drop('class', axis=1)
y = df['class']

p = X[y==0]
e = X[y==1]

outp = []
for r in p.values:
    outp.append(np.mean(np.gradient(r)))

oute = []
for r in e.values:
    oute.append(np.mean(np.gradient(r)))
plt.boxplot([outp, oute], showfliers=False)
plt.show()