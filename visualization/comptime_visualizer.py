# -*- coding: utf-8 -*-
"""
Script to analyze an array of computation times and visualize the results
@author: J. Ricardo Sanchez Ibanez (ricardosan@uma.es)
----
The example case provided corresponds to the computational times of the path
planner during the HDPR-DECOS field tests in 03/07/2019
(NOTE: Since the results of this field test are yet to be published, the txt
files are not yet available for public distribution)
"""

import numpy as np
import matplotlib.pyplot as plt

# The folder in which the .txt files are stored
folder = 'comptime_examples/'

# The names of the .txt files (These files only contain a column of numerical
# values!)
time_files = [folder + '1522 - Short1 - LocalTimeValues.txt',
              folder + '1552 - Short2 - LocalTimeValues.txt',
              folder + '1650 - Medium - LocalTimeValues.txt',
              folder + '1321 - Long - LocalTimeValues.txt'
             ]

# Names to reference each array, plus the reference to the whole set ('All')
time_names = ['Short 1', 'Short 2', 'Medium', 'Long', 'All']


times_list = []
for i,filename in enumerate(time_files):
    times_list.append(np.loadtxt(open(filename, "rb"),\
                                  delimiter=" ", skiprows=0))

# Since the original input data is in seconds, we convert it into milliseconds
for i,t in enumerate(times_list):
    times_list[i] = t*1000
    
# We output each array using bars
for i,t in enumerate(times_list):
    fig, ax = plt.subplots()
    ind = np.arange(1,len(t)+1)
    ax.bar(ind, t)
    ax.set_xticks(ind)
    ax.set_ylabel('Computational Time (ms)')

# The final plot shows the mean and standard deviation of each array, together 
# with the mean and standard deviation of the whole set of data
x_pos = np.arange(len(time_names))
mean_times = []
std_times = []
all_times = []
for i,t in enumerate(times_list):
    mean_times.append(np.mean(t))
    std_times.append(np.std(t))
    all_times = np.concatenate((all_times,t))
mean_times.append(np.mean(all_times))
std_times.append(np.std(all_times))
fig, ax = plt.subplots()
ax.bar(x_pos, mean_times, yerr=std_times, align='center', alpha=0.5,\
       ecolor='black', capsize=10)
ax.set_ylabel('Computation Time (ms)')
ax.set_xticks(x_pos)
ax.set_xticklabels(time_names)
ax.yaxis.grid(True)  