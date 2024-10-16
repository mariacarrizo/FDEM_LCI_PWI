import numpy as np
import pygimli as pg
import empymod as ep
import sys
sys.path.insert(1, 'src')

from FDEM1D import FDEM1DModelling_nosort, LCModelling

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
print('data/data_s'+sl+'_c'+co+'_u'+cr+'_nosort.npy')
print()

# Load true models

# model parameters [h_1, sigma_1, sigma_2]
model_true = np.load('models/model_s'+sl+'_c'+co+'_u'+cr+'.npy')

# Define a start model
model_ini = np.ones_like(model_true)
model_ini[:,0] = model_ini[:,0]*3   # initial thickness h_1
model_ini[:,1] = model_ini[:,1]*0.5 # initial sigma_1
model_ini[:,2] = model_ini[:,2]*0.5 # initial sigma_2

# Load true 3D data

# data parameters ['H2', 'H4', 'H8', 'P2', 'P4', 'P8', 'V2', 'V4', 'V8']
data_true = np.load('data/data_s'+sl+'_c'+co+'_u'+cr+'_nosort.npy')

# model parameters 

# number of layers
nLayers = np.shape(model_true)[1] -1

# number of measurement positions 
npos = len(data_true)

LCI = LCModelling(FDEM1DModelling_nosort)

LCI.initJacobian(dataVals=data_true, nLay=nLayers)
LCI.createJacobian(model_ini)
LCI.constraint_matrix(data_true, nLay=nLayers)
LCI.normalization(data_true, cWeight_1=1, cWeight_2=1, nLay=nLayers)
LCI.createWeight(data_true, cWeight_1=1, cWeight_2=1, nLay=nLayers)
LCI.createConstraints()

# Set transforms
#transData = pg.trans.TransLog()
transThk = pg.trans.TransLogLU(0.1,5)
transSig = pg.trans.TransLogLU(10/1000,2000/1000)

LCI.region(1).setTransModel(transThk)
LCI.region(2).setTransModel(transSig)

# Create data vector
data_true_vector = data_true.ravel()
relativeError = np.ones_like(data_true_vector)*1e-3 

# Run inversion
inv = pg.Inversion(LCI)
#inv.dataTrans = transData
model_inv = inv.run(data_true_vector, relativeError, startModel=model_ini.ravel(), verbose=False, lam=1 )

model_inv = np.array(model_inv).reshape(np.shape(model_true))
data_inv = np.array(inv.response)
data_inv = data_inv.reshape(np.shape(data_true))

np.save('results/model_inv_s'+sl+'_c'+co+'_u'+cr+'_nosort_lam1', model_inv)
np.save('results/data_inv_s'+sl+'_c'+co+'_u'+cr+'_nosort_lam1', data_inv)

print()
print('saved model in as model_inv_s'+sl+'_c'+co+'_u'+cr+'_nosort_lam1')
print('saved data as data_inv_s'+sl+'_c'+co+'_u'+cr+'_nosort_lam1')