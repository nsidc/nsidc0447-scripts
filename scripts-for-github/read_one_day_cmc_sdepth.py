#!/usr/bin/env python
# NSIDC
# Sample program to read a single day from the CMC Daily Snow Depth data
# https://nsidc.org/data/nsidc-0447
#
# Requires Python3 and the numpy and matplotlib libraries.
#
# To run:
#   python read_one_day_cmc_sdepth.py

import numpy as np
import matplotlib.pyplot as plt

#Name of file you wish to read:
file = input("Please input the file path (if applicable) and the name of the daily file you wish to read e.g. cmc_sdepth_dly_2019_v01.2.txt:\n")

#Date you wish to read in, with the format YYYYMMDD00:
sel_date = input("Please input the date you wish to view, in the YYYYMMDD00 format e.g.2019010500:\n")

string = ""
n = 706
sel_arr = np.empty(shape=(n, n))
did_colorbar = False

#Open the file and read in the selected date into an array
with open(file) as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        if line == sel_date:
            sel_arr = [np.fromstring(f.readline(), dtype=np.float, sep=' ') for i in range(n)]

#Plot the array for the selected date
imgplot = plt.imshow(sel_arr, vmin=0, vmax=50, )
if not did_colorbar:
    cbar = plt.colorbar()
    cbar.set_label("Snow depth (cm)", rotation=270)
did_colorbar = True
plt.title(sel_date)
plt.draw()
plt.pause(0.001)
input("Press [enter] to continue.")
f.close()