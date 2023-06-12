#!/usr/bin/env python3
from collections import Counter 

file = open('plaintext/txt/A.txt', 'rb')
data = file.read()
file.close()
data = data[4096:2*4096]
data = [int(b) for b in data]
bigrams = [(data[i], data[i+1]) for i in range(len(data)-1)]
cnts = Counter(bigrams)
print(len(cnts))
