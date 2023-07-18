#read in a file, write 4096 bytes at a time 
import os, sys
import pandas as pd
from collections import Counter
import subprocess

if len(sys.argv) != 4:
    print("usage: code.py dir/ class out.csv")
    print("e.g.,: code.py plaintext/pdf/ 0 pdf0.csv")
    exit(1)

data = []
inpath = sys.argv[1]
label = int(sys.argv[2])
outfile = sys.argv[3]
for f in os.listdir(inpath):
    infile = os.path.join(inpath, f)
    if '.DS_Store' in infile:
        continue
    file = open(infile, 'rb')
    _bytes = file.read()
    file.close()

    #process 4096 bytes at a time (disk block size)
    for i in range(0,len(_bytes),4096): 
        sub = _bytes[i:i+4096]
        sub = [int(x) for x in sub]

        #zero pad small data
        if len(sub) < 4096:
            diff = 4096 - len(sub)
            sub += [0] * diff
        data.append(sub)
                
    #convert to dataframe, add class label, write to csv file
    df = pd.DataFrame(data)
    df['class'] = label
    df.to_csv(outfile, index=False)

