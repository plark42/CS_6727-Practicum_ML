import numpy as np

f = open('pln.txt', 'r')
lines = f.readlines()
f.close()

filetype_sizes = {}

for line in lines:
    line = line.strip()
    size = int(line.split(' ')[0])
    filetype = line.split(' ')[1].split('/')[1]
    if filetype not in filetype_sizes:
        filetype_sizes[filetype] = []
    filetype_sizes[filetype].append(size)

for filetype in filetype_sizes:
    sizes = filetype_sizes[filetype]
    mean = np.mean(sizes)
    median = np.median(sizes)
    std = np.std(sizes)
    mn = np.min(sizes)
    mx = np.max(sizes)

    print('%s & %d & %d & %d & %d & %d \\\\ \hline' % (filetype, mean, median, std, mn, mx))
