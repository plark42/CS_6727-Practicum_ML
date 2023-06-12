import pandas as pd
import matplotlib.pyplot as plt
import sys
from collections import Counter

if len(sys.argv) != 3:
    print('usage: ./visualize.py data.csv fig.png')
    sys.exit(1)

file = sys.argv[1]
fig = sys.argv[2]
df = pd.read_csv(file)

X = df.drop('class', axis=1)
y = df['class']

# convert to byte frequency
data = []
totals = Counter(dict([(x,0) for x in range(256)]))
for row in X.values:
    counts = Counter(row)
    for c in counts:
        totals.update({c: counts[c]})
    totals = dict(sorted(totals.items()))
    data.append(list(totals.values()))    
X = pd.DataFrame(data)

#extract plaintext and encypted
plaintext = X[y == 0]
encrypted = X[y == 1]

plt.figure()
x = list(range(0,256))
plt.plot(x, plaintext.mean())
plt.plot(x, encrypted.mean())
plt.ylabel("count (N)")
plt.xlabel("ASCII number")
xticks = list(range(0,256,16))
plt.xticks(xticks, xticks, rotation=90) 
file = file.strip('csv/').strip('.').replace('.',' ')
plt.title('mean frequency of each byte (%s)' % file)
plt.legend(['plaintext', 'encrypted'])
plt.savefig(fig)
