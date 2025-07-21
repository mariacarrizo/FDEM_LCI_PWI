import numpy as np
import pygimli as pg
import emg3d 
import empymod as ep
import sys
from scipy.constants import mu_0
import matplotlib.pyplot as plt
import time
import math
from joblib import Parallel, delayed

n_workers=30

# Import model just one section

model = np.load('models/model_sinusodial.npy')
geom = np.load('data/geom_sinusoidal.npy')
data = np.load('../Sinusoidal/data_3D_Sinusoidal.npy')
topo = np.load('models/topo_sinusoidal.npy')

# Forward function

def FDEM3D_topo(geom, model_sig, model_air, height = 0.3):
    """ Simulate Dualem842S in 3D """
    startTime = time.time()
    
    frequency = 9000 # Hertz

    src_x   = geom[0]
    src_z   = geom[1]
    src_y   = geom[2]
    rec2_x  = geom[3]
    rec2_z  = geom[4]
    rec21_x = geom[5]
    rec21_z = geom[6]
    rec4_x  = geom[7]
    rec4_z  = geom[8]
    rec41_x = geom[9]
    rec41_z = geom[10]
    rec8_x  = geom[11]
    rec8_z  = geom[12]
    rec81_x = geom[13]
    rec81_z = geom[14]
    alpha   = geom[15]    
    
    # Define sources geometry
    # source = [x, y, z, azimuth, dip]
    Hsource_coords = [src_x, src_y, src_z, 0, 90 + math.degrees(alpha)]
    Vsource_coords = [src_x, src_y, src_z, 90, 0 + math.degrees(alpha)]
   # Psource_coords = Hsource_coords
    
    # Define sources
    Hsource = emg3d.TxMagneticPoint(Hsource_coords)
    Vsource = emg3d.TxMagneticPoint(Vsource_coords)
   # Psource = emg3d.TxMagneticPoint(Psource_coords)

    # Define receivers
    Hrec2 = [rec2_x, src_y, rec2_z, 0, 90 + math.degrees(alpha)]
    Vrec2 = [rec2_x, src_y, rec2_z, 90, 0 + math.degrees(alpha)]
    Prec2 = [rec21_x, src_y, rec21_z, 0, 0 + math.degrees(alpha)]
    Prec2_p = [rec21_x, src_y, rec21_z, 0, 90 + math.degrees(alpha)]

    Hrec4 = [rec4_x, src_y, rec4_z, 0, 90 + math.degrees(alpha)]
    Vrec4 = [rec4_x, src_y, rec4_z, 90, 0 + math.degrees(alpha)]
    Prec4 = [rec41_x, src_y, rec41_z, 0, 0 + math.degrees(alpha)]
    Prec4_p = [rec41_x, src_y, rec41_z, 0, 90 + math.degrees(alpha)]

    Hrec8 = [rec8_x, src_y, rec8_z, 0, 90 + math.degrees(alpha)]
    Vrec8 = [rec8_x, src_y, rec8_z, 90, 0 + math.degrees(alpha)]
    Prec8 = [rec81_x, src_y, rec81_z, 0, 0 + math.degrees(alpha)]
    Prec8_p = [rec81_x, src_y, rec81_z, 0, 90 + math.degrees(alpha)]

   # print('Hsource:', Hsource_coords)
   # print('Vsource:', Vsource_coords)
   # print('Hrec2:', Hrec2)
   # print('Vrec2:', Vrec2)
   # print('Prec2:', Prec2)
   # print('Prec2_p:', Prec2_p)
   # print('Hrec4:', Hrec4)
   # print('Vrec4:', Vrec4)
   # print('Prec4:', Prec4)
   # print('Prec4_p:', Prec4_p)
   # print('Hrec8:', Hrec8)
   # print('Vrec8:', Vrec8)
   # print('Prec8:', Prec8)
   # print('Prec8_p:', Prec8_p)
    
    # Solve Electrical fields
    print('Solving sources...')
    # Total field Hsource
    Efield_H = emg3d.solve_source(model = model_sig, source = Hsource, frequency = frequency)
    # Primary field Hsource
    Efield_H_p = emg3d.solve_source(model = model_air, source = Hsource, frequency = frequency)
    
    # Total field Vsource
    Efield_V = emg3d.solve_source(model = model_sig, source = Vsource, frequency = frequency)
    # Primary field Vsource
    Efield_V_p = emg3d.solve_source(model = model_air, source = Vsource, frequency = frequency)
    
    # Get magnetic fields
    print('getting magnetic fields...')
    # Total magnetic field Hsource
    Hfield_H = emg3d.get_magnetic_field(model = model_sig, efield = Efield_H)
    # Primary magnetic field Hsource
    Hfield_H_p = emg3d.get_magnetic_field(model = model_sig, efield = Efield_H_p)
    
    # Total magnetic field Vsource
    Hfield_V = emg3d.get_magnetic_field(model = model_sig, efield = Efield_V)
    # Primary magnetic field Vsource
    Hfield_V_p = emg3d.get_magnetic_field(model = model_air, efield = Efield_V_p)
    
    # Get fields at receivers
    print('magnetic field at receivers...')
    # For total field Hsource
    H_Hrec2 = Hfield_H.get_receiver(Hrec2)*(2j * np.pi * frequency * mu_0) 
    # For primary field Hsource
    H_Hrec2_p = Hfield_H_p.get_receiver(Hrec2)*(2j * np.pi * frequency * mu_0) 
    # Secondary field Hsource
    H_Hrec2_s = H_Hrec2 - H_Hrec2_p

    # For total field Hsource
    H_Hrec4 = Hfield_H.get_receiver(Hrec4)*(2j * np.pi * frequency * mu_0) 
    # For primary field Hsource
    H_Hrec4_p = Hfield_H_p.get_receiver(Hrec4)*(2j * np.pi * frequency * mu_0) 
    # Secondary field Hsource
    H_Hrec4_s = H_Hrec4 - H_Hrec4_p

    # For total field Hsource
    H_Hrec8 = Hfield_H.get_receiver(Hrec8)*(2j * np.pi * frequency * mu_0) 
    # For primary field Hsource
    H_Hrec8_p = Hfield_H_p.get_receiver(Hrec8)*(2j * np.pi * frequency * mu_0) 
    # Secondary field Hsource
    H_Hrec8_s = H_Hrec8 - H_Hrec8_p
    
    # For total field Vsource
    H_Vrec2 = Hfield_V.get_receiver(Vrec2)*(2j * np.pi * frequency * mu_0) 
    # For primary field Vsource
    H_Vrec2_p = Hfield_V_p.get_receiver(Vrec2)*(2j * np.pi * frequency * mu_0) 
    # Secondary field Vsource
    H_Vrec2_s = H_Vrec2 - H_Vrec2_p

    # For total field Vsource
    H_Vrec4 = Hfield_V.get_receiver(Vrec4)*(2j * np.pi * frequency * mu_0) 
    # For primary field Vsource
    H_Vrec4_p = Hfield_V_p.get_receiver(Vrec4)*(2j * np.pi * frequency * mu_0) 
    # Secondary field Vsource
    H_Vrec4_s = H_Vrec4 - H_Vrec4_p

    # For total field Vsource
    H_Vrec8 = Hfield_V.get_receiver(Vrec8)*(2j * np.pi * frequency * mu_0) 
    # For primary field Vsource
    H_Vrec8_p = Hfield_V_p.get_receiver(Vrec8)*(2j * np.pi * frequency * mu_0) 
    # Secondary field Vsource
    H_Vrec8_s = H_Vrec8 - H_Vrec8_p
    
    # For total field Psource
    H_Prec2 = Hfield_H.get_receiver(Prec2)*(2j * np.pi * frequency * mu_0) 
    # For primary field Psource in xz direction
    H_Prec2_p_xz = Hfield_H_p.get_receiver(Prec2)*(2j * np.pi * frequency * mu_0) 
    # Secondary field Psource
    H_Prec2_s = H_Prec2 - H_Prec2_p_xz
    # Primary field Psource in zz direction
    H_Prec2_p = Hfield_H_p.get_receiver(Prec2_p)*(2j * np.pi * frequency * mu_0) 

    # For total field Psource
    H_Prec4 = Hfield_H.get_receiver(Prec4)*(2j * np.pi * frequency * mu_0) 
    # For primary field Psource in xz direction
    H_Prec4_p_xz = Hfield_H_p.get_receiver(Prec4)*(2j * np.pi * frequency * mu_0) 
    # Secondary field Psource
    H_Prec4_s = H_Prec4 - H_Prec4_p_xz
    # Primary field Psource in zz direction
    H_Prec4_p = Hfield_H_p.get_receiver(Prec4_p)*(2j * np.pi * frequency * mu_0) 

    # For total field Psource
    H_Prec8 = Hfield_H.get_receiver(Prec8)*(2j * np.pi * frequency * mu_0) 
    # For primary field Psource in xz direction
    H_Prec8_p_xz = Hfield_H_p.get_receiver(Prec8)*(2j * np.pi * frequency * mu_0) 
    # Secondary field Psource
    H_Prec8_s = H_Prec8 - H_Prec8_p_xz
    # Primary field Psource in zz direction
    H_Prec8_p = Hfield_H_p.get_receiver(Prec8_p)*(2j * np.pi * frequency * mu_0) 
    
    # Calculate output components OP and IP
    print('getting output components')
    #OUT = []
    # Horizontal coplanar
    op_h2 = (H_Hrec2_s/H_Hrec2_p).imag.amp()
    ip_h2 = (H_Hrec2_s/H_Hrec2_p).real.amp()

    op_h4 = (H_Hrec4_s/H_Hrec4_p).imag.amp()
    ip_h4 = (H_Hrec4_s/H_Hrec4_p).real.amp()

    op_h8 = (H_Hrec8_s/H_Hrec8_p).imag.amp()
    ip_h8 = (H_Hrec8_s/H_Hrec8_p).real.amp()

    # Vertical coplanar
    op_v2 = (H_Vrec2_s/H_Vrec2_p).imag.amp()
    ip_v2 = (H_Vrec2_s/H_Vrec2_p).real.amp()

    op_v4 = (H_Vrec4_s/H_Vrec4_p).imag.amp()
    ip_v4 = (H_Vrec4_s/H_Vrec4_p).real.amp()

    op_v8 = (H_Vrec8_s/H_Vrec8_p).imag.amp()
    ip_v8 = (H_Vrec8_s/H_Vrec8_p).real.amp()
    
    # Perpendicular
    op_p2 = (H_Prec2_s/H_Prec2_p).imag.amp()
    ip_p2 = (H_Prec2_s/H_Prec2_p).real.amp()

    op_p4 = (H_Prec4_s/H_Prec4_p).imag.amp()
    ip_p4 = (H_Prec4_s/H_Prec4_p).real.amp()

    op_p8 = (H_Prec8_s/H_Prec8_p).imag.amp()
    ip_p8 = (H_Prec8_s/H_Prec8_p).real.amp()

    # src x pos | rec x pos | midpoint | data
  #  OUT = {'geom' : ['H2', 'H4', 'H8', 'V2', 'V4', 'V8', 'P2', 'P4', 'P8'],
  #         'src_x' : np.ones(9)*src_x,
  #         'src_y' : np.ones(9)*src_y,
  #         'rec_x' : np.hstack((rec2_x, rec4_x, rec8_x, 
  #                              rec2_x, rec4_x, rec8_x, 
  #                              rec21_x, rec41_x, rec81_x)),
  #         'midpx' : np.hstack(( src_x + 1, src_x + 2, src_x + 4,
  #                               src_x + 1, src_x + 2, src_x + 4,
  #                               src_x + 1.05, src_x + 2.05, src_x + 4.05 )),
  #         'op' : np.hstack((op_h2, op_h4, op_h8, op_v2, op_v4, op_v8, op_p2, op_p4, op_p8)),
  #         'ip' : np.hstack((ip_h2, ip_h4, ip_h8, ip_v2, ip_v4, ip_v8, ip_p2, ip_p4, ip_p8)) 
  #        }

  #  OUT = pd.DataFrame(OUT)
  #  print(OUT)
               
    endTime = time.time()
    print('Done in', (endTime - startTime), 'seconds!')

    data = np.hstack((op_h2, op_h4, op_h8, op_v2, op_v4, op_v8, op_p2, op_p4, op_p8,
                      ip_h2, ip_h4, ip_h8, ip_v2, ip_v4, ip_v8, ip_p2, ip_p4, ip_p8))
    return data

class CustomError(Exception):
    """Custom exception for specific error handling."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def FDEM25D_line_topo(sigmas, thick, topo, geom, frequency=9000,):

    if (geom[1] < topo):
        raise CustomError("wrong geometry src_z")
        
    if (geom[4] < topo):
        raise CustomError("wrong geometry rec2_z")
    
    if (geom[6] < topo):
        raise CustomError("wrong geometry rec21_z")
    
    if (geom[8] < topo):
        raise CustomError("wrong geometry rec4_z")
    
    if (geom[10] < topo):
        raise CustomError("wrong geometry rec41_z")

    if (geom[12] < topo):
        raise CustomError("wrong geometry rec8_z")

    if (geom[14] < topo):
        raise CustomError("wrong geometry rec81_z")

    src_x = geom[0]
    src_z = geom[1]
    
    sig_bg = 20/1000
    sig_air = 1/1e6

    depths = np.array([topo, topo -thick[0]])
    
    # Define mesh
    mesh = emg3d.construct_mesh(frequency = frequency,
                             properties = [sig_bg, sig_air],
                             center = [src_x, 0, src_z],
                             mapping='Conductivity',
                             domain = ([src_x - 1, src_x + 9], [-8, 8], [src_z-2, src_z+1]),
                             min_width_limits = [0.5, 0.5, 0.05], # changed z from 0.1 to 0.2
                             center_on_edge=False,
                             stretching= {'x': [1,1.5], 'y': [1.5,1.5], 'z': [1,1.5]}, 
                             lambda_from_center=True,
                             lambda_factor=3, 
                       #      cell_numbers=[512, 128, 128]
                       #      max_buffer = 300000,
                       #      min_width_pps = 5
                             )
    
    print('src x:', src_x)
    print('src z:', src_z)
    #print('rec x:', [rec2_x, rec21_x, rec4_x, rec41_x, rec8_x, rec81_x])
    #print('rec z:', [rec2_z, rec4_z, rec8_z])
    #print('alpha:', math.degrees(alpha))
    #print(mesh)
    
    # Define air layer
    sig_x = np.ones(mesh.n_cells)*sig_air # empty array to be populated
    sig_air = np.ones(mesh.n_cells)*sig_air # air array
    
    # Populate grid
    
    sig_x = np.ones(mesh.n_cells)*sig_air # empty array to be populated
    sig_air = np.ones(mesh.n_cells)*sig_air # air array
    
    x = np.ones_like(mesh.cell_centers[:,0], dtype=bool)  
    y = np.ones_like(mesh.cell_centers[:,1], dtype=bool)
    z_lay1 = (mesh.cell_centers[:,2] < depths[0]) & (mesh.cell_centers[:,2] > depths[1])
    z_lay2 = (mesh.cell_centers[:,2] < depths[1]) 
    sig_x[x*y*z_lay1] = sigmas[0] # First layer sigma
    sig_x[x*y*z_lay2] = sigmas[1] # Second layer sigma
    
    
    #  4. Define models
    
    Model = emg3d.Model(mesh, 
                     property_x = sig_x,
                     mapping = 'Conductivity')
    
    Model_air = emg3d.Model(mesh,
                         property_x = sig_air,
                         mapping = 'Conductivity')

    data_3D = FDEM3D_topo(geom, 
                              Model, 
                              Model_air)

    return data_3D

class FDEM25DModelling(pg.frameworks.Modelling):
    
    def __init__(self, nlay, topo, geom):
        self.nlay = nlay
        self.topo = topo
        self.geom = geom
        Mesh = pg.meshtools.createMesh1DBlock(nlay)
        super().__init__()
        self.setMesh(Mesh)
        print('Initialized')
                   
    def response(self, par):
        """ Compute response vector for a certain model [mod] 
        par = [thickness_1, thickness_2, ..., thickness_n, sigma_1, sigma_2, ..., sigma_n]
        """
        print('sigma:', np.asarray(par)[self.nlay-1:self.nlay*2-1])
        print('thicks:', np.asarray(par)[:self.nlay-1])
        resp = FDEM25D_line_topo(sigmas = np.asarray(par)[self.nlay-1:self.nlay*2-1],   # sigma
                                 thick = np.asarray(par)[:self.nlay-1],                  # thickness
                                 topo = self.topo,
                                 geom = self.geom
                      )
        return resp
    
    def response_mt(self, par, i=0):
        """Multi-threaded forward response."""
        return self.response(par)
    
    def createJacobian(self, par, dx=1e-4):
        """ compute Jacobian for a 1D model """
        resp = self.response(par)
        n_rows = len(resp) # number of data values in data vector
        n_cols = len(par) # number of model parameters
        J = self.jacobian() # we define first this as the jacobian
        J.resize(n_rows, n_cols)
        Jt = np.zeros((n_cols, n_rows))
        for j in range(n_cols):
            mod_plus_dx = par.copy()
            mod_plus_dx[j] += dx
            Jt[j,:] = (self.response(mod_plus_dx) - resp)/dx # J.T in col j
        for i in range(n_rows):
            J[i] = Jt[:,i]

nlay = np.shape(model)[1] - 1

startTime = time.time()

model_inv = []
response = []

for i in range(15,45):
    nsrcx = i
    nmdpx = nsrcx + 4
    
    fop = FDEM25DModelling(nlay=nlay, topo = topo[nmdpx], geom=geom[nsrcx])
    
    transThk = pg.trans.TransLogLU(0.1,1)
    transSig = pg.trans.TransLogLU(5/1000,300/1000)
    
    fop.region(0).setTransModel(transThk)
    fop.region(1).setTransModel(transSig)
    
    # Perform inversion in each position
    
    startModel = np.array([0.6, 0.05, 0.05]) # initial model
    
    data_p = data[nsrcx]
    
    rel_err = np.ones_like(data_p)*1e-3 
    inv = pg.Inversion(fop)
    model_inv.append(inv.run(dataVals=data_p, errorVals=rel_err, startModel=startModel, verbose=True, lam=0 ))
    response.append(inv.response)
    
print()
endTime = time.time()
print('Done in', (endTime - startTime), 'seconds!')

#OUT_dataframe = pd.concat(OUT)

#np.save('data/data_s1_c1_uc', OUT)
np.save('models/Inversion_Sinu_Models', np.array(model_inv))
np.save('models/Inversion_Sinu_Responses', np.array(response))
    