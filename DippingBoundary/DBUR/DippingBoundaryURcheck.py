# 3D forward dipping boundary

# Script to create synthetic 3D data

import numpy as np
import emg3d 
import empymod as ep
import pandas as pd
from scipy.constants import mu_0
import matplotlib.pyplot as plt
import time
from joblib import Parallel, delayed
import sys
sys.path.insert(1, 'src')

# 0. Define instrument settings

height = 0.15
frequency = 9000
n_workers = 20

# Define angles to test

alpha = np.arange(-10,10)
alphasr = np.deg2rad(alpha)

sigmas = np.array([[20/1000, 200/1000],
                   [20/1000, 400/1000],
                   [20/1000, 800/1000],
                   [20/1000, 1600/1000]])

# 5. Simulate data

def Dualem842_3D(xsrc, Model, Model_air, frequency=frequency, height=height):
   # print('Position:', p)
    print('Defining geometry')
    # Define source coordinates
    src_x = xsrc
    Hsrc_coords = [src_x, 0, height, 0, 90]
    Vsrc_coords = [src_x, 0, height, 90, 0]
    print('source:', Hsrc_coords)
    
    # Define H and V receivers coordinates
    offsets_HV = np.array([src_x+2, src_x+4, src_x+8])
    #print('offsets:',offsets_HV)
    #rec_coords = [offsets_HV, offsets_HV*0, np.ones_like(offsets_HV)*height, azi, dip]
    
    # Define P receivers coordinates
    offsets_P = np.array([src_x+2.1, src_x+4.1, src_x+8.1])
    #rec_coords_p = [offsets_P, offsets_P*0, np.ones_like(offsets_P)*height, azi, dip]
    
    # Define sources
    Hsource = emg3d.TxMagneticPoint(Hsrc_coords)
    Vsource = emg3d.TxMagneticPoint(Vsrc_coords)
    
    # Solve Electrical fields
    #print('Solving sources...')
    # Total field Hsource
    Efield_H = emg3d.solve_source(model = Model, source = Hsource, frequency = frequency)
    # Primary field Hsource
    Efield_H_p = emg3d.solve_source(model = Model_air, source = Hsource, frequency = frequency)
    
    # Total field Vsource
    Efield_V = emg3d.solve_source(model = Model, source = Vsource, frequency = frequency)
    # Primary field Vsource
    Efield_V_p = emg3d.solve_source(model = Model_air, source = Vsource, frequency = frequency)

    # Get magnetic fields
   # print('getting magnetic fields...')
    # Total magnetic field Hsource
    Hfield_H = emg3d.get_magnetic_field(model = Model, efield = Efield_H)
    # Primary magnetic field Hsource
    Hfield_H_p = emg3d.get_magnetic_field(model = Model_air, efield = Efield_H_p)
    
    # Total magnetic field Vsource
    Hfield_V = emg3d.get_magnetic_field(model = Model, efield = Efield_V)
    # Primary magnetic field Vsource
    Hfield_V_p = emg3d.get_magnetic_field(model = Model_air, efield = Efield_V_p)
    
    # Get fields at receivers
  #  print('magnetic field at receivers...')
    # For total field Hsource
    H_Hrec = Hfield_H.get_receiver((offsets_HV, offsets_HV*0, height, 0, 90))*(2j * np.pi * frequency * mu_0) 
    # For primary field Hsource
    H_Hrec_p = Hfield_H_p.get_receiver((offsets_HV, offsets_HV*0, height, 0, 90))*(2j * np.pi * frequency * mu_0) 
    # Secondary field Hsource
    H_Hrec_s = H_Hrec - H_Hrec_p
    
    # For total field Vsource
    H_Vrec = Hfield_V.get_receiver((offsets_HV, offsets_HV*0, height, 90, 0))*(2j * np.pi * frequency * mu_0) 
    # For primary field Vsource
    H_Vrec_p = Hfield_V_p.get_receiver((offsets_HV, offsets_HV*0, height, 90, 0))*(2j * np.pi * frequency * mu_0) 
    # Secondary field Vsource
    H_Vrec_s = H_Vrec - H_Vrec_p
    
    # For total field Psource
    H_Prec = Hfield_H.get_receiver((offsets_P, offsets_P*0, height, 0, 0))*(2j * np.pi * frequency * mu_0) 
    # For primary field Psource in xz direction
    H_Prec_p_xz = Hfield_H_p.get_receiver((offsets_P, offsets_P*0, height, 0, 0))*(2j * np.pi * frequency * mu_0) 
    # Secondary field Psource
    H_Prec_s = H_Prec - H_Prec_p_xz
    # Primary field Psource in zz direction
    H_Prec_p = Hfield_H_p.get_receiver((offsets_P, offsets_P*0, height, 0, 90))*(2j * np.pi * frequency * mu_0)
    
     # Calculate output components OP and IP
 #   print('getting output components')
    # Horizontal coplanar
    op_h = (H_Hrec_s/H_Hrec_p).imag.amp()
    ip_h = (H_Hrec_s/H_Hrec_p).real.amp()
    #OUT.append([op_h, ip_h])
    # Vertical coplanar
    op_v = (H_Vrec_s/H_Vrec_p).imag.amp()
    ip_v = (H_Vrec_s/H_Vrec_p).real.amp()
    #OUT.append([op_v, ip_v])
    # Perpendicular
    op_p = (H_Prec_s/H_Prec_p).imag.amp()
    ip_p = (H_Prec_s/H_Prec_p).real.amp()
    #OUT.append([op_p, ip_p])
    
 #   OUT_i = pd.DataFrame({'geom'  : ['H2', 'H4', 'H8', 'V2', 'V4', 'V8', 'P2', 'P4', 'P8'],
 #                         'src_x' : [Hsrc_coords[0], Hsrc_coords[0], Hsrc_coords[0],
 #                                    Vsrc_coords[0], Vsrc_coords[0], Vsrc_coords[0],
 #                                    Hsrc_coords[0], Hsrc_coords[0], Hsrc_coords[0]],
 #                         'rec_x' : np.hstack((offsets_HV, offsets_HV, offsets_P)),
 #                         'midpx' : np.hstack((Hsrc_coords[0] + (offsets_HV - Hsrc_coords[0])/2,
 #                                              Vsrc_coords[0] + (offsets_HV - Vsrc_coords[0])/2,
 #                                              Hsrc_coords[0] + (offsets_P - Hsrc_coords[0])/2)),
 #                         'op'    : np.hstack((op_h, op_v, op_p)),
 #                         'ip'    : np.hstack((ip_h, ip_v, ip_p)) 
 #                         })
    
    #OUT = pd.concat([OUT, OUT_i], ignore_index=True)
    print()
    return np.array([op_h, op_p, op_v, ip_h, ip_p, ip_v]).ravel()

def ForwardDippingBoundary(alpha, sigmas):
    print('Running: alpha: ', np.degrees(alpha), 'sigma1: ', sigmas[0]*1000, 'sigma2: ', sigmas[1]*1000)
    
    xsrc = 11 # at 11 meters, since the center of the dipping boundary is at 15 m
    mdp = xsrc + 4
    
    pos = np.arange(0,30)
    h1 = np.ones_like(pos, dtype=float)*4
    h1[:mdp] = h1[:mdp] - np.flip(pos[:mdp]) * np.tan(alpha)
    h1[mdp-1:] = h1[mdp-1:] + pos[:mdp+1]* np.tan(alpha)
    
    # 1. Create a 2D model
    
    s1 = np.ones_like(h1)*sigmas[0]/1000
    s2 = np.ones_like(h1)*sigmas[1]/1000
    model = np.vstack((h1,s1,s2)).T
    npos = np.shape(model)[0]      # number of positions
    nlay = np.shape(model)[1] - 1  # number of layers
    
    depths = np.zeros((npos, nlay))
    depths[:,1] = - model[:,0]

    print('depts:', depths)
    
    # 2. Create a mesh
    
    # Define a homogoneous model
    sig = np.array([100/1000])
    thk = np.array([])
    
    # Insert air layer
    sig_3d = np.hstack(([1/1e6], sig))
    depth_3d = np.hstack(([0], -np.cumsum(thk)))
    
    # mesh
    mesh = emg3d.construct_mesh(frequency = frequency,
                             properties = [20/1000, 20/1000, sig_3d[0]],
                             center = [mdp,0,height],
                             mapping='Conductivity',
                             domain = ([xsrc-10, xsrc+18],[-10, 10],[-10,10]),
                             min_width_limits = [0.2, 0.2, 0.1], # changed z from 0.1 to 0.2
                             center_on_edge=False,
                             stretching= {'x': [1,1.5], 'y': [1.1,1.5], 'z': [1,1.5]}, 
                             lambda_from_center=True,
                             lambda_factor=3, 
                       #      cell_numbers=[512, 128, 128]
                       #      max_buffer = 300000,
                       #      min_width_pps = 5
                             )
    
    # 3. Populate mesh

    if not np.all(h1 > 0):
        bad_vals = h1[h1 < 0]
        raise ValueError(f"Array contains non-positive values: {bad_vals}")
    
    # Define air layer
    sig_x = np.ones(mesh.n_cells)*sig_3d[0] # empty array to be populated
    sig_air = np.ones(mesh.n_cells)*sig_3d[0] # air array

    x = mesh.cell_centers[:,0] <=0
    y = np.ones_like(mesh.cell_centers[:,1], dtype=bool)
    z_lay1 = (mesh.cell_centers[:,2] < depths[0,0]) & (mesh.cell_centers[:,2] > depths[0,1])
    z_lay2 = (mesh.cell_centers[:,2] < depths[0,1]) 
    
    sig_x[x*y*z_lay1] = model[0,1] # First layer sigma
    sig_x[x*y*z_lay2] = model[0,2] # Second layer sigma
    
    for p in range(npos):
       
        x = (mesh.cell_centers[:,0] >= p) & (mesh.cell_centers[:,0] < p+1)
        y = np.ones_like(mesh.cell_centers[:,1], dtype=bool)
        z_lay1 = (mesh.cell_centers[:,2] < depths[p,0]) & (mesh.cell_centers[:,2] > depths[p,1])
        z_lay2 = (mesh.cell_centers[:,2] < depths[p,1]) 
    
        sig_x[x*y*z_lay1] = model[p,1]
        sig_x[x*y*z_lay2] = model[p,2]
    
    # fill after position npos
    
    x = (mesh.cell_centers[:,0] > npos) 
    y = np.ones_like(mesh.cell_centers[:,1], dtype=bool)
    z_lay1 = (mesh.cell_centers[:,2] < depths[-1,0]) & (mesh.cell_centers[:,2] > depths[-1,1])
    z_lay2 = (mesh.cell_centers[:,2] < depths[-1,1]) 
    
    sig_x[x*y*z_lay1] = model[-1,1]
    sig_x[x*y*z_lay2] = model[-1,2]
    
    #  4. Define models
    
    Model = emg3d.Model(mesh, 
                     property_x = sig_x,
                     mapping = 'Conductivity')
    
    Model_air = emg3d.Model(mesh,
                         property_x = sig_air,
                         mapping = 'Conductivity')

#    data = Dualem842_3D(xsrc, Model, Model_air)

#    return data

startTime = time.time()

OUT = Parallel(n_jobs=1,verbose=0)(delayed(ForwardDippingBoundary)(ai, si) for ai in alphasr for si in sigmas)    

endTime = time.time()

print()
print('Done in', (endTime - startTime), 'seconds!')

#np.save('dataUR', OUT)
