#!/usr/bin/env python3
from feature_extraction import get_features 
import sys
import pickle
from collections import Counter

DATAPATH = '/Users/fac_rubin/Documents/GeorgiaTech/CS_6727-Practicum/data/'

def main():
    if len(sys.argv) != 3:
        print('usage: ./test_model.py model.pkl test.txt')
        exit(1)

    f = open(sys.argv[1], 'rb')
    random_forest = pickle.load(f)
    f.close()

    f = open(sys.argv[2], 'r')
    files = f.readlines()
    f.close()

    n = 0
    for f in files:
        f = f.strip()
        n += 1
        print(n, 'of', len(files), f, file=sys.stderr)
        infile = DATAPATH + f
        datafile = open(infile, 'rb')
        _bytes = datafile.read()
        datafile.close()

        pred = []
        for i in range(0, len(_bytes), 4096):
            data = _bytes[i:i+4096]
            if len(data) < 4096:
                diff = 4096 - len(data)
                data += bytes(diff) 

            features = get_features(data)
            yp = random_forest.predict(features)
            pred.append(yp[0])
    
        counts = Counter(pred)

        pred = ','.join([str(x) for x in pred])
        output = '%s; %s; pln=%d; enc=%d' % (f, pred, counts[0], counts[1])
        print(output)
        print(output, file=sys.stderr)


if __name__ == '__main__':
    main()
