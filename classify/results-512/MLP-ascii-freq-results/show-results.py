#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

columns = ['algorithm', 'filetype', 'accuracy', 'precision', 'recall']
results = pd.read_csv('MLP-ascii-freq-results.csv', header=None, sep=' ', names=columns)

def plot_results_algorithm(algo):    
    i = results['algorithm'] == algo
    data = results[i].drop('algorithm', axis=1)
    data.plot.bar(x='filetype')
    plt.legend(loc='lower right')
    plt.title('MLP classification results: %s vs. plaintext' % algo.upper())
    plt.ylabel('percentage (%)')
    plt.yticks(range(0,101,20))

def plot_results_filetype(filetype):
    i = results['filetype'] == filetype
    data = results[i].drop('filetype', axis=1)
    data.plot.bar(x='algorithm')
    plt.legend(loc='lower right')
    plt.title('MLP classification results: %s vs. plaintext' % filetype.upper())
    plt.ylabel('percentage (%)')
    plt.yticks(range(0,101,20))

    
for algo in np.unique(results.algorithm):    
    plot_results_algorithm(algo)

for filetype in np.unique(results.filetype):    
    plot_results_filetype(filetype)    
