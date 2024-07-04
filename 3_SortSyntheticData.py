# Script to sort data

import numpy as np
import pandas as pd

# 1. Upload data

DATA = np.load('data/data_s1_c1_uc.pkl', allow_pickle=True)

# 2. Sort data by coil geometry

DATA_sorted = DATA.sort_values(by='geom')

# 3. Define number of position

n_coil_geom = 9 # Number of coil geometries

npos = int(len(DATA_sorted)/n_coil_geom) # number of positions

# number of data parameters per position

n_data_param = 18

# We have 3 additional points to the left of the first midpoint (assuming 
# 1 position per meter)
DATA_sorted_midpoint = np.zeros((npos-3, n_data_param))

# We will have positions with insufficient data in the edges

pos=0
for p in range(-3,npos):
    dat = np.hstack((DATA_sorted.loc[(DATA_sorted.midpx > p+.06) & (DATA_sorted.midpx <=p +1.06)]['op'],
                     DATA_sorted.loc[(DATA_sorted.midpx > p+.06) & (DATA_sorted.midpx <=p +1.06)]['ip'])) 
    if dat.size == 0:
        continue
    if dat.size == 18:
        DATA_sorted_midpoint[pos,:] = dat
        pos += 1
        print('position: ', pos)
        print('location: ')
        print(DATA_sorted.loc[(DATA_sorted.midpx > p+.06) & (DATA_sorted.midpx <p +1.06)])
    print()

np.save('data/data_s1_c1_uc_sort', DATA_sorted_midpoint)