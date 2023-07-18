#!/usr/bin/env python3
import os
import numpy as np

train = [[],[],[],[],[]]
test  = [[],[],[],[],[]]

#for each plaintext directory and file
for dirpath, dirnames, filenames in sorted(os.walk('plaintext')):
    
    #deal only with files (not dirs)
    if len(dirnames) == 0:
        
        #ignore .DS_Store
        if ".DS_Store" in filenames:
            filenames.remove('.DS_Store')

        #get the full path including filetype
        filenames = ['%s/%s' % (dirpath, f) for f in sorted(filenames)]
        
        #split into 5 sets 
        groups = np.array_split(filenames,5)
        
        #divy up into training and testing
        for i in range(5):
            group = groups[i]
            tmp = list(filenames)
            for g in group:
                test[i].append(str(g))
                tmp.remove(g)
            for f in tmp:
                train[i].append(f)
        
#for each training sample, add the equivalent encrypted files 
final_train = [[],[],[],[],[]]
for i in range(5):
    for p_file in train[i]:
        for enc in ['aes', 'bf', 'cha', 'des3', 'rc4']:
            s = 'encrypted/%s' % (enc)
            e_file = p_file.replace('plaintext', s)
            e_file = e_file + '.%s' % enc
            final_train[i].append(p_file)
            final_train[i].append(e_file)
            
#for each training sample, add the equivalent encrypted files 
final_test = [[],[],[],[],[]]
for i in range(5):
    for p_file in test[i]:
        for enc in ['aes', 'bf', 'cha', 'des3', 'rc4']:
            s = 'encrypted/%s' % (enc)
            e_file = p_file.replace('plaintext', s)
            e_file = e_file + '.%s' % enc
            final_test[i].append(p_file)
            final_test[i].append(e_file)
            
for i in range(5):
    s = 'train_%d.txt' % (i+1)
    f = open(s, 'w')
    for filename in final_train[i]:
        f.write(filename + '\n')
    f.close()    
    
for i in range(5):
    s = 'test_%d.txt' % (i+1)
    f = open(s, 'w')
    for filename in final_test[i]:
        f.write(filename + '\n')
    f.close()   