#!/usr/bin/env python3
from feature_extraction import get_features 
import sys
import pickle
from collections import Counter

DATAPATH = '/Users/fac_rubin/Documents/GeorgiaTech/CS_6727-Practicum/data/'

mimes = ['application/gzip', 'application/octet-stream', 'application/pdf', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/x-dosexec', 'application/x-executable', 'application/x-mach-binary', 'application/x-mach-binary\ntmp (for architecture x86_64):\t', 'application/zip', 'audio/mpeg', 'audio/x-wav', 'image/gif', 'image/jpeg', 'image/png', 'text/html', 'text/plain', 'video/mp4', 'video/quicktime']

columns = ['kurtosis', 'entropy', 'stdev', 'pi', 'mse',\
         'chi', 'p', 'autocorr', 'mean', 'bigrams', 'ics',\
         'hmean', 'skew', 'mime', 'class']

pd.set_option('mode.use_inf_as_na', True)

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
#!/usr/bin/env python3
from feature_extraction import get_features 
from sklearn.preprocessing import LabelEncoder 
import subprocess
import sys, pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

DATAPATH = '/Users/fac_rubin/Documents/GeorgiaTech/CS_6727-Practicum/data/'

mimes = ['application/gzip', 'application/octet-stream', 'application/pdf', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/x-dosexec', 'application/x-executable', 'application/x-mach-binary', 'application/x-mach-binary\ntmp (for architecture x86_64):\t', 'application/zip', 'audio/mpeg', 'audio/x-wav', 'image/gif', 'image/jpeg', 'image/png', 'text/html', 'text/plain', 'video/mp4', 'video/quicktime']

columns = ['kurtosis', 'entropy', 'stdev', 'pi', 'mse',\
         'chi', 'p', 'autocorr', 'mean', 'bigrams', 'ics',\
         'hmean', 'skew', 'mime', 'class']

pd.set_option('mode.use_inf_as_na', True)

if len(sys.argv) != 3:
    print('usage: ./train_model.py training.txt model.pkl')
    exit(1)

training_data = pd.DataFrame(columns=columns)

labelEncoder = LabelEncoder()
labelEncoder.fit(mimes)

with open(sys.argv[1], 'r') as file:
    for line in file:
        infile = DATAPATH + line.strip()
        print('processing', infile)
        datafile = open(infile, 'rb')
        _bytes = datafile.read()
        datafile.close()

        #read first 4096 bytes, get "file" type from cmd line
        sub = _bytes[0:4096]
        f = open('tmp', 'wb')
        f.write(sub)
        f.close()
        retval = subprocess.check_output(['file', '-bI', 'tmp'])
        mime = retval.decode('utf-8').split('; ')[0]
        mime = labelEncoder.transform([mime])[0]

        for i in range(0, len(_bytes), 4096):
            data = _bytes[i:i+4096]
            if len(data) < 4096:
                diff = 4096 - len(data)
                data += bytes(diff) 

            features = get_features(data)
            features['mime'] = mime
            if 'plaintext' in infile:
                features['class'] = 0
            else:
                features['class'] = 1
            print(features)
            training_data = pd.concat([training_data, features])

random_forest = RandomForestClassifier()
X = training_data.drop('class', axis=1)
X.fillna(0, inplace=True)
y = training_data['class'].astype('int')
random_forest.fit(X,y)

with open(sys.argv[2], 'wb') as f:
    pickle.dump(random_forest, f)

