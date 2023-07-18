#!/usr/bin/env python3
import warnings
warnings.simplefilter(action='ignore', category=Warning)

import glob, os, math
import pandas as pd
import numpy as np
from collections import Counter
from scipy.stats import entropy, kurtosis, chisquare, hmean, skew
from sklearn.metrics import mean_squared_error

#returns list of 256 values..
def ascii_freqs(row): 
    totals = [(x,0) for x in range(256)]
    totals = Counter(dict(totals))
    counts = Counter(row)
    for c in counts:    
        totals.update({c: counts[c]}) 
    return [totals[i] for i in totals]

columns = ['algorithm', 'filetype', 'kurtosis', 'entropy', 'stdev', 'pi', 'mse',\
           'chi', 'p', 'autocorr', 'mean', 'bigrams', 'ics', 'hmean', 'skew', \
               'class']
data = pd.DataFrame(columns=columns)

csvfiles = glob.glob('*.*.csv')
filenum = 1
for f in csvfiles:
    algorithm = f.split('.')[0]
    filetype = f.split('.')[1]
    print(algorithm, filetype, filenum, 'of', len(csvfiles))
    filenum += 1
    
    df = pd.read_csv(f)
    X = df.drop('class', axis=1)
    
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
    
    #compute monti carlo pi of each row
    pis = []
    for row in X.values:
        hits = 0
        for i in range(0,len(row),4):
            b0 = hex(row[i])
            b1 = hex(row[i+1]).strip('0x')
            x = int(b0+b1, 16) 
            b0 = hex(row[i+2])
            b1 = hex(row[i+3]).strip('0x')
            y = int(b0+b1, 16)
            x = x / (2**16)
            y = y / (2**16)
            if math.sqrt((x**2) + (y**2)) <= 1.0:
                hits += 1
        pi = 4.0 * (hits / (len(row)/4))
        pis.append(pi)
    pis = pd.Series(pis)
        
    #compare sorted row to line; compute mse
    norm = np.linspace(start=0, stop=255, num=4096, dtype='int')
    mse = []
    for row in X.values:
        x = sorted(row)
        mse.append(mean_squared_error(norm, x))
    mse = pd.Series(mse)        
    
    #convert each row to byte count (4096 to 256)
    Xp = []
    for row in X.values:
        freq = ascii_freqs(row)
        Xp.append(freq)

    # each row is now a byte count 
    X = pd.DataFrame(Xp)
    
    #compute index of coincidence 
    ics = []
    c = 256.0
    N = 4096
    factor = N * (N-1) / c
    for row in X.values:
        total = 0
        for i in range(256):
            n = row[i]
            total += n * (n-1)
        ic = total / factor
        ics.append(ic)
    ics = pd.Series(ics)
    
    rows = pd.DataFrame(columns=columns)    
    rows['class'] = df['class']
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
    rows['ics'] = ics
    rows['hmean'] = hmean(X,axis=1)
    rows['skew'] = skew(X,axis=1)
    rows['pi'] = pis
    rows['mse'] = mse
    data = pd.concat([data, rows])

data.to_csv('features.csv', index=False)
# os.system('./rm_plaintext_duplicates.sh')
    

    
        