import numpy as np 

import math 

 

mu, sigma = 1.5, 0.5 # mean and standard deviation 

s = np.random.lognormal(mu, sigma, 1000) 

n = len(s) 

 

# write data to a file 

with open('data.dat', 'w') as outfile: 

    for value in s: 

        outfile.write("%f\n" % value) 

    outfile.close() 

 

# read data from a file 

with open('data.dat', 'r') as infile: 

    s = [float(value) for value in infile.readlines()] 

    infile.close() 

 

# generate a histogram 

import matplotlib.pyplot as plt 

count, bins, ignored = plt.hist(s, 200, density=True, align='mid') 

 

# superimpose a lognormal distribution pdf 

x = np.linspace(min(bins), max(bins), 10000) 

pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) 

       / (x * sigma * np.sqrt(2 * np.pi))) 

plt.plot(x, pdf, linewidth=2, color='r') 

 

 

# estimate parameters from data 

sum = 0 

for v in s: 

    sum = sum + np.log(v) 

mu = sum / n 

 

sum = 0 

for v in s: 

    sum = sum + (np.log(v) - mu)**2 

sigma = math.sqrt(sum / n) 

 

x = np.linspace(min(bins), max(bins), 10000) 

pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) 

       / (x * sigma * np.sqrt(2 * np.pi))) 

plt.plot(x, pdf, linewidth=2, color='y') 

 

 

plt.axis('tight') 

plt.show() 
