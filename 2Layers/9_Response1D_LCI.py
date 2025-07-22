import numpy as np
import pygimli as pg
import empymod as ep
import sys
sys.path.insert(1, '../src')

from FDEM1D import FDEM1DModelling

sl = sys.argv[1]
co = sys.argv[2]
cr = sys.argv[3]

print('Model parameters:')
print('slope: ', sl)
print('contrast: ', co)
print('cond or res c/v: ', cr)
print()

print('Using files:')
print('results/model_inv_s'+sl+'_c'+co+'_u'+cr+'_lam1.npy')

model = np.load('results/model_inv_s'+sl+'_c'+co+'_u'+cr+'_lam1.npy')

fop_1D = FDEM1DModelling(height=0.15)

npos = len(model)

data_1D = []

for pos in range(npos):
    data_1D.append(fop_1D.response(model[pos]))
    
np.save('results/data_inv_s'+sl+'_c'+co+'_u'+cr+'_lam1.npy', data_1D)