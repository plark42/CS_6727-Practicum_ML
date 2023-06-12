#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('features.csv')

#for filetype in np.unique(df['filetype']):
for filetype in ['zip']:
    cond1 = df['filetype'] == filetype
    cond2 = df['class'] == 1
    data = df[cond1 & cond2]
    
    cond1 = df['class'] == 0
    cond2 = df['algorithm'] == 'aes'
    cond3 = df['filetype'] == filetype
    plain = df[cond1 & cond2 & cond3]
    plain['algorithm'] = 'plaintext'
    data = pd.concat([data, plain])
    
    data.boxplot(column='entropy', by='algorithm', showfliers=False)
    plt.title('entropy %s' % filetype)
    plt.suptitle('')
    
    data.boxplot(column='kurtosis', by='algorithm', showfliers=False)
    plt.title('kurtosis %s' % filetype)
    plt.suptitle('')

    data.boxplot(column='stdev', by='algorithm', showfliers=False)
    plt.title('stdev %s' % filetype)
    plt.suptitle('')

    data.boxplot(column='chisquare', by='algorithm', showfliers=False)
    plt.title('chisquare %s' % filetype)
    plt.suptitle('')
