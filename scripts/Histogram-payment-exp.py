#!/usr/bin/python3
import numpy as np 
import scipy.stats
import math 
 

# read data from a file 

with open('data/Pay-time.csv', 'r') as infile: 

    s = [float(value) for value in infile.readlines()] 

    infile.close() 

n = len(s) 
bincount = math.ceil(n/5)

# generate a histogram 

import matplotlib.pyplot as plt 

count, bins, ignored = plt.hist(s, bincount, density=True, align='mid') 


 

# estimate parameters from data 
# exponential

sum = 0 

for v in s: 

    sum = sum  + v

a = 1
b = sum/n/a



x = np.linspace(min(bins), max(bins), bincount) 

#a exponential distribution
pdf = (np.exp(-x/b))/b

plt.plot(x, pdf, linewidth=2, color='y') 


print(bincount, b)
print(scipy.stats.chisquare(count,pdf))

 

plt.axis('tight') 

plt.savefig("demo.pdf") 
