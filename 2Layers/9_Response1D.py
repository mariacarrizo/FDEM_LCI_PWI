import numpy as np
import pygimli as pg
import empymod as ep
import sys
sys.path.insert(1, 'src')

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
print('models/model_s'+sl+'_c'+co+'_u'+cr+'.npy')

model_true = np.load('models/model_s'+sl+'_c'+co+'_u'+cr+'.npy')

fop_1D = FDEM1DModelling()

npos = len(model_true)

data_1D = []

for pos in range(npos):
    data_1D.append(fop_1D.response(model_true[pos]))
    
np.save('data/data_s'+sl+'_c'+co+'_u'+cr+'_1D.npy', data_1D)