import numpy as np
import emg3d 
import empymod as ep
import pandas as pd
from scipy.constants import mu_0
import math
import time
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

# Load models
m_topo = np.load('../models/model_3DChannel_topo_full.npy')
topo = np.load('../models/topo.npy')
topo_ = np.load('../models/topo_.npy')

Sim_Model = emg3d.load('../Sim_Model.h5')
sim = Sim_Model['simulation']
Model = sim.model
mesh = sim.model.grid

Sim_Model_air = emg3d.load('../Sim_Model_air.h5')
sim = Sim_Model_air['simulation']
Model_air = sim.model

## 0. Define instrument settings

height = 0.15
frequency = 9000
n_workers = 40

# 1. Load model

# model with air layer

depths_air = -m_topo[:,:,0]
depths = np.stack((depths_air, -m_topo[:,:,0]-m_topo[:,:,1]), axis=2)


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

    print('Hsource:', Hsource_coords)
    print('Vsource:', Vsource_coords)
    print('Hrec2:', Hrec2)
    print('Vrec2:', Vrec2)
    print('Prec2:', Prec2)
    print('Prec2_p:', Prec2_p)
    print('Hrec4:', Hrec4)
    print('Vrec4:', Vrec4)
    print('Prec4:', Prec4)
    print('Prec4_p:', Prec4_p)
    print('Hrec8:', Hrec8)
    print('Vrec8:', Vrec8)
    print('Prec8:', Prec8)
    print('Prec8_p:', Prec8_p)
    
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
    OUT = {'geom' : ['H2', 'H4', 'H8', 'V2', 'V4', 'V8', 'P2', 'P4', 'P8'],
           'src_x' : np.ones(9)*src_x,
           'src_y' : np.ones(9)*src_y,
           'rec_x' : np.hstack((rec2_x, rec4_x, rec8_x, 
                                rec2_x, rec4_x, rec8_x, 
                                rec21_x, rec41_x, rec81_x)),
           'rec_y' : np.ones(9)*src_y,
           'midpx' : np.hstack(( src_x + 1, src_x + 2, src_x + 4,
                                 src_x + 1, src_x + 2, src_x + 4,
                                 src_x + 1.05, src_x + 2.05, src_x + 4.05 )),
           'op' : np.hstack((op_h2, op_h4, op_h8, op_v2, op_v4, op_v8, op_p2, op_p4, op_p8)),
           'ip' : np.hstack((ip_h2, ip_h4, ip_h8, ip_v2, ip_v4, ip_v8, ip_p2, ip_p4, ip_p8)) 
          }

    OUT = pd.DataFrame(OUT)
    print(OUT)
               
    endTime = time.time()
    print('Done in', (endTime - startTime), 'seconds!')
    return OUT

def FDEM3D_line_topo(geom, depths=depths, model=Model, model_air=Model_air, frequency=9000, ):

    src_x = geom[0]
    src_z = geom[1]
    src_y = geom[2]
    
    sig_bg = 20/1000
    sig_air = 1/1e6

   # npos = len(model)

    # Define mesh
    mesh = emg3d.construct_mesh(frequency = frequency,
                             properties = [sig_bg, sig_bg, sig_air],
                             center = [src_x, 0, src_z],
                             mapping='Conductivity',
                             domain = ([src_x - 20, src_x + 20], [-10, 10], [src_z-6, src_z+4]),
                             min_width_limits = [0.2, 0.2, 0.05], # changed z from 0.1 to 0.2
                             center_on_edge=False,
                             stretching= {'x': [1,1.5], 'y': [1.1,1.5], 'z': [1.1,1.5]}, 
                             lambda_from_center=True,
                             lambda_factor=3, 
                       #      cell_numbers=[512, 128, 128]
                       #      max_buffer = 300000,
                       #      min_width_pps = 5
                             )

    print('src x:', src_x)
    print('src z:', src_z)
    print('src y:', src_y)
    #print('rec x:', [rec2_x, rec21_x, rec4_x, rec41_x, rec8_x, rec81_x])
    #print('rec z:', [rec2_z, rec4_z, rec8_z])
    #print('alpha:', math.degrees(alpha))
    print(mesh)
    
    
    #  4. Define models
    
    Model = model.interpolate_to_grid(mesh)
    
    Model_air = emg3d.Model(mesh,
                         property_x = sig_air,
                         mapping = 'Conductivity')

    data_3D = FDEM3D_topo(geom, 
                          Model, 
                          Model_air)

    return data_3D

# Define the source and receivers geometry

nrows = 60
h0 = 0.3 # height of instrument

xx = np.linspace(-9, 51, 60, endpoint=False)
yy = np.linspace(-9, 51, 60, endpoint=False)

xx_ = np.linspace(-10, 50, 60, endpoint=False)
yy_ = np.linspace(-10, 50, 60, endpoint=False)

geom = []

for r in range(nrows):

    dz = topo_[:,r] - topo[:,r]
    dx = xx_ - xx
    
    h0 = 0.3 # height of the midpoint 
    
    alphas = np.arctan(-dz/dx)
    
    mdp_z = -topo[:,r] + (h0 / np.cos(alphas))
    mdp_x = xx_ + h0 * np.sin(alphas)
    
    src_x = mdp_x * np.cos(alphas)  - 4
    src_z = mdp_z + (mdp_x - src_x)*np.sin(alphas)
    src_y = np.ones_like(src_x)* yy_[r]
    
    rec2_x = mdp_x * np.cos(alphas)  - 2
    rec2_z = mdp_z + (mdp_x - rec2_x)*np.sin(alphas)
    
    rec21_x = mdp_x * np.cos(alphas)  - 1.9
    rec21_z = mdp_z + (mdp_x - rec21_x)*np.sin(alphas)
    
    rec4_x = mdp_x.copy()
    rec4_z = mdp_z.copy()
    
    rec41_x = mdp_x * np.cos(alphas)  + 0.1
    rec41_z = mdp_z + (mdp_x - rec41_x)*np.sin(alphas)
    
    rec8_x = mdp_x * np.cos(alphas)  + 4
    rec8_z = mdp_z + (mdp_x - rec8_x)*np.sin(alphas)
    
    rec81_x = mdp_x * np.cos(alphas)  + 4.1
    rec81_z = mdp_z + (mdp_x - rec81_x)*np.sin(alphas)
    
    geom.append(np.array([src_x, src_z, src_y, rec2_x, rec2_z, rec21_x, rec21_z, 
                                   rec4_x, rec4_z, rec41_x, rec41_z,
                                   rec8_x, rec8_z, rec81_x, rec81_z, alphas]).T)

geom_full = np.array(geom).reshape(3600,16)

startTime = time.time()

OUT = Parallel(n_jobs=50, verbose=0)(delayed(FDEM3D_line_topo)(geo) for geo in geom_full)
             
print()
endTime = time.time()
print('Done in', (endTime - startTime), 'seconds!')

OUT_dataframe = pd.concat(OUT)

OUT_dataframe.to_pickle('../data/data_3DChannel_topo.pkl')