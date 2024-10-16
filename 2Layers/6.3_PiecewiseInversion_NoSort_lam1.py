import numpy as np
import pygimli as pg
import empymod as ep
import sys
sys.path.insert(1, 'src')

from FDEM1D import FDEM1DModelling_nosort

sl = sys.argv[1]
co = sys.argv[2]
cr = sys.argv[3]

print('Model parameters:')
print('slope: ', sl)
print('contrast: ', co)
print('cond or res c/v: ', cr)
print()

print('Using files:')
#print('models/model_s'+sl+'_c'+co+'_u'+cr+'.npy')
print('data/data_s'+sl+'_c'+co+'_u'+cr+'_nosort.npy')
print()

# Load true data
data_true = np.load('data/data_s'+sl+'_c'+co+'_u'+cr+'_nosort.npy')

# number of measurement positions 
npos = len(data_true)

# Setting forward operator 

fop = FDEM1DModelling_nosort(nlay=2)

transThk = pg.trans.TransLogLU(0.1,6)
transSig = pg.trans.TransLogLU(10/1000,2000/1000)

fop.region(0).setTransModel(transThk)
fop.region(1).setTransModel(transSig)

# Perform inversion in each position

startModel = np.array([3, 0.5, 0.5]) # initial model

model_inv = []
response = []

for pos in range(npos):
    dat = data_true[pos]
    rel_err = np.ones_like(dat)*1e-3 
    inv = pg.Inversion(fop)
    model_inv.append(inv.run(dataVals=dat, errorVals=rel_err, startModel=startModel, verbose=False, lam=1 ))
    response.append(inv.response)
    
# Save estimated model

np.save('results/model_inv_s'+sl+'_c'+co+'_u'+cr+'_1D_nosort_lam1', model_inv)
np.save('results/data_inv_s'+sl+'_c'+co+'_u'+cr+'_1D_nosort_lam1', response)