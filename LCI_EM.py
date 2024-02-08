## LCI Inversion

import numpy as np
import pygimli as pg
import empymod as ep
from scipy.constants import mu_0
import matplotlib.pyplot as plt
import sys
sys.path.insert(1, 'src')

from showStitched import showStitchedModels

# Example for 3 layered model
nLayers=3

# Set 1D forward function with empymod
class fop1d():
    """ 1D FDEM response 
        
    Parameters
    ----------
    sgm : array
           Array of electrical conductivities [S/m], len(sigma) = nlay
    thk : array
           Array of thicknesses [m], len(thk) = nlay - 1
    Freq : frequency of device [Hz]
    coilOrient : array of strings
                  coil orientations: 'H' for horizontal coplanar, 
                  'V' for vertical coplanar, 'P' for perpendicular
    coilSpacing : array
                    separations of the transmitter and receiver coils [m]
    height : float
                height of the device with respect to ground [m]
    Returns
    -------
    Array [OP, IP]

    """  
    def __init__(self, Freq, coilOrient, coilSpacing, height):
        """ initialize class """
        
        self.Freq = Freq
        self.coilOrient = coilOrient
        self.coilSpacing = coilSpacing
        self.height = height
    
    def em1d(self, sgm, thk):
        # Source and receivers geometry [x, y, z]
        source    = [0, 0, -self.height]
        receivers = [self.coilSpacing, np.zeros(len(self.coilSpacing)), -self.height]
        # Depth and resistivity
        res_air = 1e6
        res = np.hstack((res_air, 1/sgm))
        depth = np.hstack((0, np.cumsum(thk)))
        # Empty array to store responses
        OUT = []

        if any(coilOrient == 'H'):

            H_Hs = ep.dipole(source, receivers, depth, res, self.Freq, ab = 66, xdirect=None, 
                              verb=0)*(2j * np.pi * self.Freq * mu_0) 
            H_Hp = ep.dipole(source, receivers, depth=[], res=[res_air], freqtime = self.Freq,
                             ab = 66, verb=0)*(2j * np.pi * self.Freq * mu_0)   
            op = (H_Hs/H_Hp).imag.amp() 
            ip = (H_Hs/H_Hp).real.amp() 
            OUT.append([op, ip])

        if any(coilOrient == 'V'):
            V_Hs = ep.dipole(source, receivers, depth, res, self.Freq, ab =55, xdirect=None, 
                             verb=0)*(2j * np.pi * self.Freq * mu_0) 
            V_Hp = ep.dipole(source, receivers, depth=[], res=[res_air], freqtime=self.Freq,ab=55, 
                             verb=0)*(2j * np.pi * self.Freq * mu_0)
            op = (V_Hs/V_Hp).imag.amp() 
            ip = (V_Hs/V_Hp).real.amp() 
            OUT.append([op, ip])

        if any(coilOrient == 'P'):
            # Maybe put 0.1m in receiver offset
            P_Hs = ep.dipole(source, receivers, depth, res, self.Freq, ab=46, xdirect=None, 
                             verb=0)*(2j * np.pi * self.Freq * mu_0) 
            P_Hp = ep.dipole(source, receivers, depth=[], res=[res_air], freqtime= self.Freq,
                             ab=66, verb=0)*(2j * np.pi * self.Freq * mu_0) 
            op = (P_Hs/P_Hp).imag.amp() 
            ip = (P_Hs/P_Hp).real.amp() 

            OUT.append([op, ip])

        return np.array(OUT).ravel()  
    
# Class for 1D forward modelling with pygimli
class FDEM1D(pg.frameworks.Modelling):
    """ Class forward modelling Frequency Domain EM data """
    def __init__(self, nLayers=nLayers):
        """ Initialize class and set survey configuration """
        self.nLayers = nLayers
        mesh = pg.meshtools.createMesh1DBlock(self.nLayers)
        super().__init__()
        self.setMesh(mesh)
        
    def response(self, mod):
        """ Compute response vector for a certain model [mod] 
        mod = [thickness_1, thickness_2, ..., thickness_n, sigma_1, sigma_2, ..., sigma_n]
        """
        resp = fop1d.em1d(np.asarray(mod)[self.nLayers-1:self.nLayers*2-1],   # sigma
                       np.asarray(mod)[:self.nLayers-1]                  # thickness
                       )
        return resp
    
    def response_mt(self, mod, i=0):
        """Multi-threaded forward response."""
        return self.response(mod)
    
    def createJacobian(self, mod, dx=1e-8):
        """ compute Jacobian for a 1D model """
        resp = self.response(mod)
        n_rows = len(resp) # number of data values in data vector
        n_cols = len(mod) # number of model parameters
        J = self.jacobian() # we define first this as the jacobian
        J.resize(n_rows, n_cols)
        Jt = np.zeros((n_cols, n_rows))
        for j in range(n_cols):
            mod_plus_dx = mod.copy()
            mod_plus_dx[j] += dx
            Jt[j,:] = (self.response(mod_plus_dx) - resp)/dx # J.T in col j
        for i in range(n_rows):
            J[i] = Jt[:,i]
    
    def createDefaultStartModel(self, mod):
        """ create default start model 1D """
        model_0 = pg.Vector([2, 2, 20/1000, 20/1000, 20/1000])
        return model_0
    
# LC Modelling class
class LCModelling(pg.frameworks.LCModelling):
    """2D Laterally constrained (LC) modelling.
    """

    def __init__(self, fop, **kwargs):
        """Parameters: fop class ."""
        super().__init__(fop, **kwargs)
        self._singleRegion = False
        self._fopTemplate = fop
        self._fopKwargs = kwargs
        self._fops1D = []
        self._mesh = None
        self._nSoundings = 0
        self._parPerSounding = 0
        self._jac = None
        self.soundingPos = None

    def setDataBasis(self, **kwargs):
        """Set homogeneous data basis.
        Set a common data basis to all forward operators.
        If you want individual you need to set them manually.
        """
        for f in self._fops1D:
            f.setDataBasis(**kwargs)

    def initModelSpace(self, nLayers):
        """Initialize model space."""
        for i, f in enumerate(self._fops1D):
            f.initModelSpace(nLayers)

    def createDefaultStartModel(self, models):
        """Create default starting model."""
        sm = pg.Vector()
        for i, f in enumerate(self._fops1D):
            sm = pg.cat(sm, f.createDefaultStartModel(models[i]))
        return sm

    def response(self, par):
        """Cut together forward responses of all soundings."""
        mods = np.asarray(par).reshape(self._nSoundings, self._parPerSounding)
        resp = pg.Vector(0)
        for i in range(self._nSoundings):
            r = self._fops1D[i].response(mods[i])
            resp = pg.cat(resp, r)
        return resp

    def createJacobian(self, par):
        """Create Jacobian matrix by creating individual Jacobians."""
        mods = np.asarray(par).reshape(self._nSoundings, self._parPerSounding)
        for i in range(self._nSoundings):
            self._fops1D[i].createJacobian(mods[i])
        
    def initJacobian(self, dataVals, nLayers, nPar=1):
        """Initialize Jacobian matrix.
        Parameters
        ----------
        dataVals : ndarray | RMatrix | list
            Data values of size (nSounding x Data per sounding).
            All data per sounding need to be equal in length.
            If they don't fit into a matrix use list of sounding data.
        """
        nSoundings = len(dataVals)

        self.createParametrization(nSoundings, nLayers=nLayers, nPar=nPar)

        if self._jac is not None:
            self._jac.clear()
        else:
            self._jac = pg.matrix.BlockMatrix()

        self.fops1D = []
        nData = 0

        for i in range(nSoundings):
            kwargs = {}
            for key, val in self._fopKwargs.items():
                if hasattr(val, '__iter__'):
                    kwargs[key] = val[i] 
                else:
                    kwargs[key] = val

            f = None
            if issubclass(self._fopTemplate, pg.frameworks.Modelling):
                f = self._fopTemplate(**kwargs)
            else:
                f = type(self._fopTemplate)(self.verbose, **kwargs)

            f.setMultiThreadJacobian(self._parPerSounding)

            self._fops1D.append(f)

            nID = self._jac.addMatrix(f.jacobian())
            self._jac.addMatrixEntry(nID, nData, self._parPerSounding * i)
            nData += len(dataVals[i])
            
        self._jac.recalcMatrixSize()
        #print("Jacobian size:", self._jac.rows(), self._jac.cols(), nData)
        self.setJacobian(self._jac)
        return self._jac

    def constraint_matrix(self, dataVals, nLayers):
        """ Create constraint matrix

        Parameters
        ----------
            dataVals : list of 1D pyGIMLi data vectors (nSounding x Data per sounding) [list]
            nLayers : number of layers (for blocky inversion) [int]
        """

        nSoundings = len(dataVals) # number of soundings
        
        boundaries_thk = (nLayers - 1) * (nSoundings - 1) # inner mesh boundaries for thicknesses
        boundaries_sig = nLayers * (nSoundings - 1) # inner mesh boundaries for conductivities

        CM = np.zeros((boundaries_thk + boundaries_sig, (nLayers*2 - 1) * nSoundings))
        h = -np.eye(1, nLayers * 2) + np.eye(1, nLayers * 2, k = (nLayers * 2 - 1))

        for i in range(boundaries_thk + boundaries_sig):
            CM[i, i:h.shape[1]+i] = h

        print('Size of constraint matrix:', np.shape(CM))

        self.CM = pg.utils.toSparseMatrix(CM) # convert to sparse pg matrix

        return self.CM
    
    def createWeight(self, dataVals, cWeight_1, cWeight_2, nLayers):
        """ Create constraint weights (cWeights)
            Blocky model : vertical constraint weights for both model parameter regions

        Parameters
        ----------
            dataVals : list of 1D pyGIMLi data vectors [list]
            cWeight_1 : thickness constraint weight (blocky model) [float]
            cWeight_2 : resistivity constraint weight (blocky model) [float]
            nLayers : number of layers (for blocky inversion) [int]
        """
        nSoundings = len(dataVals) # number of soundings
        
        """ constraint weights for blocky model """
        cWeight_thk = cWeight_1
        cWeight_sig = cWeight_2

        boundaries_thk = (nLayers - 1) * (nSoundings - 1)
        boundaries_sig = nLayers * (nSoundings - 1)

        cWeight_thk = pg.Vector(boundaries_thk, cWeight_thk)

        cWeight_sig = pg.Vector(boundaries_sig, cWeight_sig)

        self.cWeight = pg.cat(cWeight_thk, cWeight_sig)
        print('shape of Constraint cWeight:', np.shape(self.cWeight))
        
    def createConstraints(self):
        """ create weighted constraint matrix """
        self._CW = pg.matrix.LMultRMatrix(self.CM, self.cWeight) # , verbose = True)
        self.setConstraints(self._CW)

    def drawModel(self, ax, model, **kwargs):
        """Draw models as stitched 1D model section."""
        mods = np.asarray(model).reshape(self._nSoundings,
                                         self._parPerSounding)
        pg.viewer.mpl.showStitchedModels(mods, ax=ax, useMesh=True,
                                         x=self.soundingPos,
                                         **kwargs)

# LC Inversion class
class LCInversion(pg.Inversion):
    """Quasi-2D Laterally constrained inversion (LCI) framework."""

    def __init__(self, fop, **kwargs):
        super(LCInversion, self).__init__(fop=fop, **kwargs)
        
    def prepare(self, dataVals, errorVals, nLayers, **kwargs):
        """Prepare inversion with given data and error vectors."""
        
        dataVec = pg.RVector3()
        for d in dataVals:
            dataVec = pg.cat(dataVec, d)

        errVec = pg.RVector3()
        for e in errorVals:
            errVec = pg.cat(errVec, e)

        self.fop.initJacobian(dataVals=dataVals, nLayers=nLayers, nPar=1)
        
        # self.fop.initJacobian resets prior set startmodels
        if self._startModel is not None:
            self.fop.setStartModel(self._startModel)
        rC = self.fop.regionManager().regionCount()

        if kwargs.pop('disableLCI', False):
            self.inv.setMarquardtScheme(0.7)
            # self.inv.setLocalRegularization(True)
            for r in self.fop.regionManager().regionIdxs():
                self.fop.setRegionProperties(r, cType=0)
        else:
            # self.inv.stopAtChi1(False)
            cType = kwargs.pop('cType', None)
            if cType is None:
                cType = [1] * rC

            zWeight = kwargs.pop('zWeight', None)
            if zWeight is None:
                zWeight = [0.0] * rC

            self.fop.setRegionProperties('*',
                                         cType=cType,
                                         zWeight=zWeight,
                                         **kwargs)
            self.inv.setReferenceModel(self.fop.startModel())

        return dataVec, errVec
    
    def run(self, dataVals, errorVals, nLayers, **kwargs):
        """Run inversion with given data and error vectors."""
        lam = kwargs.pop('lam', 20)
        dataVec, errVec = self.prepare(dataVals, errorVals, nLayers, **kwargs)
        print('#'*50)
        print(kwargs)
        print('#'*50)
        return super(LCInversion, self).run(dataVec, errVec, lam=lam, **kwargs)

# Set problem
Freq = 9000
coilOrient = np.array(['H', 'V', 'P'])
coilSpacing = np.array([2, 4, 8])
nLayers = 3 # careful: nlay must be equal in 1Dfop and LC
height = 0

# Initialize forward operator function with empymod
fop1d = fop1d(Freq, coilOrient, coilSpacing, height)

# Initialize forward modeller with pygimli
FOP = FDEM1D()

# True models
pos = 10 # number of soundings

x =  np.linspace(0,pos,pos, endpoint=False)
sigm_1 = 10/1000 
sigm_2 = 20/1000
sigm_3 = 40/1000
thk_1 = 1/5*x + 1
thk_2 = 2 - 1/7*x

models = np.zeros((pos, nLayers*2-1))
models[:,0] = thk_1
models[:,1] = thk_2
models[:,2] = sigm_1
models[:,3] = sigm_2
models[:,4] = sigm_3

# Simulate data for each 1D model
data = []
for p in range(pos):
    data.append(FOP.response(models[p]))
# Define error vector
relativeError = np.ones_like(data)*1e-3
    
# Initialize LCModelling class
LC = LCModelling(FDEM1D)

# Initialize inversion class
inv = LCInversion(LC)

# Run inversion
models_est = inv.run(data, relativeError, nLayers=nLayers)


