#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('features.csv')
i = df['class'] == 0
df.loc[i,'algorithm'] = 'none'

for filetype in np.unique(df['filetype']):   
    i = df['filetype'] == filetype
    data = df[i]
    
    columns = list(df.columns)
    for s in ['algorithm', 'filetype', 'class']:
        columns.remove(s)

    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(10,10)) # create 2x2 array of subplots
    for r in range(4):
        for c in range(3):
            i = (r*3) + c 
            data.boxplot(column=columns[i], by='algorithm', showfliers=False, ax=axes[r,c])
            xticks = axes[r,c].get_xticklabels()
            yticks = axes[r,c].get_yticks()
            axes[r,c].set_yticklabels(['%.2f' % y for y in yticks], fontsize=8)
            axes[r,c].set_xlabel('')
            axes[r,c].set_ylabel(columns[i], fontsize=8)
            axes[r,c].set_title('')

    axes[3,1].set_xlabel('encryption')
    plt.tight_layout()
    plt.suptitle(filetype)
    plt.show()
      

