#!/usr/bin/python3
import numpy as np 
import scipy.stats
import math 
 

# read data from a file 

with open('data/Pickup-time.csv', 'r') as infile: 

    s = [float(value) for value in infile.readlines()] 

    infile.close() 

n = len(s) 
bincount = math.ciel(n/5)

# generate a histogram 

import matplotlib.pyplot as plt 

count, bins, ignored = plt.hist(s, bincount, density=True, align='mid') 


 

# estimate parameters from data 

sum = 0 

for v in s: 

    sum = sum + np.log(v) 

mu = sum / n 

 

sum = 0 

for v in s: 

    sum = sum + (np.log(v) - mu)**2 

sigma = math.sqrt(sum / n) 



x = np.linspace(min(bins), max(bins), bincount) 

pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) 

       / (x * sigma * np.sqrt(2 * np.pi))) 

plt.plot(x, pdf, linewidth=2, color='y') 


print(scipy.stats.chisquare(count,pdf))

 

plt.axis('tight') 

plt.savefig("demo.pdf") 
