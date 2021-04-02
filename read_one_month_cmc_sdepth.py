#!/usr/bin/env python
# NSIDC
# Sample program to read a single month from the CMC Monthly Snow Depth data
# https://nsidc.org/data/nsidc-0447
#
# Requires Python3 and the numpy and matplotlib libraries.
#
# To run:
#   python read_one_month_cmc_sdepth.py

import numpy as np
import matplotlib.pyplot as plt

#Name of file you wish to read in
file = input("Please input the file path (if applicable) and the name of the file you wish to read in e.g. cmc_sdepth_mly_2019_v01.2.txt:\n")

# Year and month you wish to look at
year = file[15:19] #this is read from the filename
month = input("Please input the month you wish to view e.g. for February input 2:\n") #this is user input

#Set up various variables including the size of the array
space = '           '
sel_date = year + space + month
string = ""
n = 706
sel_arr = np.empty(shape=(n, n))
did_colorbar = False

#Open the file and read in the array for the selected month
with open(file) as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        if line == sel_date:
            sel_arr = [np.fromstring(f.readline(), dtype=np.float, sep=' ') for i in range(n)]

#Plot the array for the selected month
imgplot = plt.imshow(sel_arr, vmin=0, vmax=50)
if not did_colorbar:
    cbar = plt.colorbar()
    cbar.set_label('Snow depth (cm)', rotation=270)
did_colorbar = True
plt.title(sel_date)
plt.draw()
plt.pause(0.001)
input("Press [enter] to continue.")
f.close()