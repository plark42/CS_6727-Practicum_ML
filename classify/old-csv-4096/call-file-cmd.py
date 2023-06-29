#!/usr/bin/env python3

import glob 
import pandas as pd
import subprocess

for f in glob.glob('*.*.csv'):
    algorithm = f.split('.')[0]
    filetype = f.split('.')[1]
    print(algorithm, filetype)
    
    df = pd.read_csv(f)
    X = df.drop('class', axis=1)
    y = df['class']
    
    for i, row in enumerate(X.values):    
        b = bytes(row)
        file = open('tmp', 'wb')
        file.write(b)
        file.close()
        retval = str(subprocess.check_output(['file', '-b', 'tmp']))
        print(algorithm, filetype, retval.split('; ')[0], y[i])