#!/usr/bin/env python
# NSIDC
# Sample program to read CMC Daily Snow Depth data
# https://nsidc.org/data/nsidc-0447
#
# Requires Python3 and the numpy and matplotlib libraries.
#
# To run:
#   python read_all_cmc_daily_sdepth.py
#
import numpy as np
import matplotlib.pyplot as plt

#Name of the daily snow depth file you wish to read
file = 'cmc_sdepth_dly_2019_v01.2.txt'

#Open the file and set the size of the array to read the data into
f = open(file, 'r')
string = ""
n = 706
arr = np.empty(shape=(n, n))
did_colorbar = False

# Read in a single day into an array, plot the array then move on to the next day.
while 1:
    i = 0
    while i < n:
        line = f.readline()
        if not line:
            break
        if (len(line) <= 20):
            date = line
        else:
            arr[i] = np.fromstring(line, dtype=np.float, sep=' ')
            i += 1
    imgplot = plt.imshow(arr, vmin=0, vmax=50)
    if not did_colorbar:
        cbar = plt.colorbar()
        cbar.set_label('Snow depth (cm)', rotation=270)
    did_colorbar = True
    plt.title(date)
    plt.draw()
    plt.pause(0.001)
    input("Press [enter] to plot the next day. Or if you wish to quit press 'Ctrl' + 'C' then enter")

f.close()
