#!/usr/bin/env python3
import warnings
warnings.simplefilter(action='ignore', category=Warning)

import glob 
import pandas as pd
from collections import Counter
from scipy.stats import entropy, kurtosis, chisquare

#returns list of 256 values..
def ascii_freqs(row): 
    totals = [(x,0) for x in range(256)]
    totals = Counter(dict(totals))
    counts = Counter(row)
    for c in counts:    
        totals.update({c: counts[c]}) 
    return [totals[i] for i in totals]

columns = ['algorithm', 'filetype', 'kurtosis', 'entropy', 'stdev', 'chi', 'p', 'autocorr', 'mean', 'bigrams', 'mime', 'class']
data = pd.DataFrame(columns=columns)

for f in glob.glob('*.*.csv'):
    algorithm = f.split('.')[0]
    filetype = f.split('.')[1]
    print(algorithm, filetype)
    
    df = pd.read_csv(f)
    X = df.drop(['class', 'mime'], axis=1)
    y = df['class']
    mime = df['mime']
    
    #compute autocorrelation (serial corr) of each row
    autocorr = []
    for row in X.values:
        ac = pd.Series(row).autocorr()
        autocorr.append(ac)
    autocorr = pd.Series(autocorr)
    
    #compute count of bigrams
    bigrams = []
    for row in X.values:    
        bg = [(row[i], row[i+1]) for i in range(len(row)-1)]
        cnts = len(Counter(bg))
        bigrams.append(cnts)
    bigrams = pd.Series(bigrams)
    
    #compute mean of each row
    mean = X.mean(axis=1)
    mean = pd.Series(mean)
    
    #convert each row to byte count (4096 to 256)
    Xp = []
    for row in X.values:
        freq = ascii_freqs(row)
        Xp.append(freq)
    
    X = pd.DataFrame(Xp)
    rows = pd.DataFrame(columns=columns)    
    rows['class'] = y
    rows['mime'] = mime
    rows['algorithm'] = algorithm
    rows['filetype'] = filetype
    rows['kurtosis'] = kurtosis(X, axis=1)
    rows['entropy'] = entropy(X, axis=1)
    rows['stdev'] = X.std(axis=1)  
    rows['chi'] = chisquare(X, axis=1)[0]    
    rows['p'] = chisquare(X, axis=1)[1]
    rows['autocorr'] = autocorr
    rows['mean'] = mean
    rows['bigrams'] = bigrams
    
    data = pd.concat([data, rows])

data.to_csv('features.csv', index=False)
    

    
        
