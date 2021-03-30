# NSIDC
# Sample program to read a single month from the CMC Monthly SWE averages
# https://nsidc.org/data/nsidc-0447
#
# Requires Python3 and the numpy and matplotlib libraries.
#
# To run:
#   python read_one_month_cmc_swe.py

import numpy as np
import matplotlib.pyplot as plt

#Name of the file you wish to read in
file = input( "Please input the file path (if applicable) and file name for the file you wish to read e.g. cmc_swe_mly_1998to2019_v01.2.txt:\n")

#Year and month you wish to look at
year = input("Please input the year you wish to read e.g. 2000:\n")
month = input("Please input the month you wish to read e.g. 2:\n")

#Set up various variables including the size of the array
if int(month) < 10:
    space = '           '
else:
    space = '          '
space2 = '        '
no = '4631'
sel_date = year + space + month + space2 + no
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
    cbar.set_label('SWE (mm)', rotation=270)
did_colorbar = True
plt.title(sel_date)
plt.draw()
plt.pause(0.001)
input("Press [enter] to continue.")
f.close()