#read in plaintext files
#read in 1 disk block of bytes
#encrypt using AES, 3DES, Blowfish
import os

KEY = 'password'

#for each directory in plaintext/ 
for d in os.listdir('plaintext'):
    inpath = os.path.join('plaintext', d)
    outpath = os.path.join('encrypted', 'des3', d)

    #skip non directories
    if not os.path.isdir(inpath):
        continue

    #create directory in encrypted/ if does not exist
    if os.path.exists(outpath) == False:
        os.mkdir(outpath)

    #get each plaintext file in this directory
    for f in os.listdir(inpath):
        if '.DS_Store' in f:
            continue
        infile = os.path.join(inpath, f)
        outfile = os.path.join(outpath, f + '.des3')
        cmd = 'openssl enc -des3 -pass pass:%s -nosalt -in %s -out %s' % (KEY, infile, outfile)
        print('encrypting %s' % f)
        os.system(cmd)

