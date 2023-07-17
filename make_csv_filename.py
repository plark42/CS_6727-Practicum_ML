#read in a file, write 4096 bytes at a time 
import os, sys
import pandas as pd
from collections import Counter
import subprocess

if len(sys.argv) != 4:
    print("usage: code.py dir/ class out.csv")
    print("e.g.,: code.py plaintext/pdf/ 0 pdf0.csv")
    exit(1)

inpath = sys.argv[1]
label = int(sys.argv[2])
outfile = sys.argv[3]

columns = list(range(4096))
columns += ['mime', 'filename', 'class']
df = pd.DataFrame(columns=columns)

for filename in os.listdir(inpath):
    data = []
    infile = os.path.join(inpath, filename)
    if '.DS_Store' in infile:
        continue
    f = open(infile, 'rb')
    _bytes = f.read()
    f.close()

    #read first 4096 bytes, get "file" type from cmd line
    sub = _bytes[0:4096]
    f = open('tmp', 'wb')
    f.write(sub)
    f.close()
    retval = subprocess.check_output(['file', '-bI', 'tmp'])
    mime = retval.decode('utf-8').split('; ')[0]

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
    rows = pd.DataFrame(data)
    rows['class'] = label
    rows['filename'] = filename
    rows['mime'] = mime
    df = pd.concat([df, rows])

df.to_csv(outfile, index=False)
