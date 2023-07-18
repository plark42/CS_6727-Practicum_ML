import pandas as pd
import sys
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

#returns list of 256 values..
def ascii_freqs(row): 
    totals = [(x,0) for x in range(256)]
    totals = Counter(dict(totals))
    counts = Counter(row)
    for c in counts:    
        totals.update({c: counts[c]}) 
    freq = [totals[i] for i in totals]
    return freq

if len(sys.argv) != 3:
    print('usage: code.py input.csv output.csv')
    exit(1)

infile = sys.argv[1]
outfile = sys.argv[2]

df = pd.read_csv(infile)
X = df.drop('class', axis=1)
y = df['class']

data = []
for row in X.values:
    freq = ascii_freqs(row)
    data.append(freq)

X = pd.DataFrame(data)
X['class'] = y
X.to_csv(outfile, index=False)


# pandas magic to get frequency of each ASCII character
#bins = np.arange(0,257)
#freq = pd.cut(row, bins=bins, right=False, include_lowest=True).value_counts().sort_index()
#data.append(freq.values)
