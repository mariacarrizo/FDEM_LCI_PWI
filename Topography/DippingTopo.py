# 3D Forward dipping topography

# 3D Forward dipping topography

import numpy as np
import emg3d 
import empymod as ep
import pandas as pd
from scipy.constants import mu_0
import math
import time
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import sys
sys.path.insert(1, '../src')

n_workers=20

# Now testing with topography

def FDEM3D_topo(geom, model_sig, model_air, height = 0.15):
    """ Simulate Dualem842S in 3D """
    startTime = time.time()
    
    frequency = 9000 # Hertz

    src_x = geom[0]
    src_z = geom[1]
    rec2_x = geom[2]
    rec2_z = geom[3]
    rec4_x = geom[4]
    rec4_z = geom[5]
    rec8_x = geom[6]
    rec8_z = geom[7]
    rec21_x = geom[8]
    rec41_x = geom[9]
    rec81_x = geom[10]
    alpha = geom[11]
    
    # Define sources geometry
    # source = [x, y, z, azimuth, dip]
    Hsource_coords = [src_x, 0, src_z, 0, 90 + math.degrees(alpha)]
    Vsource_coords = [src_x, 0, src_z, 90, 0 + math.degrees(alpha)]
   # Psource_coords = Hsource_coords
    
    # Define sources
    Hsource = emg3d.TxMagneticPoint(Hsource_coords)
    Vsource = emg3d.TxMagneticPoint(Vsource_coords)
   # Psource = emg3d.TxMagneticPoint(Psource_coords)

    # Define receivers
    Hrec2 = [rec2_x, 0, rec2_z, 0, 90 + math.degrees(alpha)]
    Vrec2 = [rec2_x, 0, rec2_z, 90, 0 + math.degrees(alpha)]
    Prec2 = [rec21_x, 0, rec2_z, 0, 0 + math.degrees(alpha)]
    Prec2_p = [rec21_x, 0, rec2_z, 0, 90 + math.degrees(alpha)]

    Hrec4 = [rec4_x, 0, rec4_z, 0, 90 + math.degrees(alpha)]
    Vrec4 = [rec4_x, 0, rec4_z, 90, 0 + math.degrees(alpha)]
    Prec4 = [rec41_x, 0, rec4_z, 0, 0 + math.degrees(alpha)]
    Prec4_p = [rec41_x, 0, rec4_z, 0, 90 + math.degrees(alpha)]

    Hrec8 = [rec8_x, 0, rec8_z, 0, 90 + math.degrees(alpha)]
    Vrec8 = [rec8_x, 0, rec8_z, 90, 0 + math.degrees(alpha)]
    Prec8 = [rec81_x, 0, rec8_z, 0, 0 + math.degrees(alpha)]
    Prec8_p = [rec81_x, 0, rec8_z, 0, 90 + math.degrees(alpha)]

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
 #   OUT = {'src_x' : [Hsource_coords[0], Hsource_coords[0], Hsource_coords[0],
 #                     Vsource_coords[0], Vsource_coords[0], Vsource_coords[0],
 #                     Hsource_coords[0], Hsource_coords[0], Hsource_coords[0]],
 #          'rec_x' : np.hstack((offsets_H, offsets_V, offsets_P)),
 #          'midpx' : np.hstack(((offsets_H - Hsource_coords[0])/2,
 #                               (offsets_V - Vsource_coords[0])/2,
 #                               (offsets_P - Hsource_coords[0])/2)),
 #          'op' : np.hstack((op_h, op_v, op_p)),
 #          'ip' : np.hstack((ip_h, ip_v, ip_p)) 
 #         }
               
    endTime = time.time()
    print('Done in', (endTime - startTime), 'seconds!')
    return np.array([op_h2, op_h4, op_h8, op_p2, op_p4, op_p8, op_v2, op_v4, op_v8,
                     ip_h2, ip_h4, ip_h8, ip_p2, ip_p4, ip_p8, ip_v2, ip_v4, ip_v8]).ravel()

def FDEM3D_line_topo(geom, depths, model, frequency=9000):

    src_x = geom[0]
    src_z = geom[1]
    
    sig_bg = 20/1000
    sig_air = 1/1e6

    npos = len(model)

    # Define mesh
    mesh = emg3d.construct_mesh(frequency = frequency,
                             properties = [sig_bg, sig_air],
                             center = [src_x, 0, src_z],
                             mapping='Conductivity',
                             domain = ([src_x - 10, src_x + 10], [-10, 10], [src_z-10, src_z+10]),
                             min_width_limits = [0.2, 0.2, 0.1], # changed z from 0.1 to 0.2
                             center_on_edge=False,
                             stretching= {'x': [1,1.5], 'y': [1.1,1.5], 'z': [1.1,1.5]}, 
                             lambda_from_center=True,
                             lambda_factor=3, 
                       #      cell_numbers=[512, 128, 128]
                       #      max_buffer = 300000,
                       #      min_width_pps = 5
                             )

   # print('src x:', src_x)
   # print('src z:', src_z)
   # print('rec x:', [rec2_x, rec21_x, rec4_x, rec41_x, rec8_x, rec81_x])
   # print('rec z:', [rec2_z, rec4_z, rec8_z])
   # print('alpha:', math.degrees(alpha))
    print(mesh)
    
    # Define air layer
    sig_x = np.ones(mesh.n_cells)*sig_air # empty array to be populated
    sig_air = np.ones(mesh.n_cells)*sig_air # air array
    
    # Populate grid
    
    # Fill before position 0
    
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

    data_3D = FDEM3D_topo(geom, 
                          Model, 
                          Model_air)

    return data_3D

def ForwardDippingTopo(theta, sigma):
    xsrc = 11
    mdp = xsrc + 4
    
    x = np.arange(0,30, dtype=float)
    h_a = np.zeros_like(x, dtype=float)
    h_a[:mdp] = h_a[:mdp] - np.flip(x[:mdp]) * np.tan(theta)
    h_a[mdp-1:] = h_a[mdp-1:] + x[:mdp+1]* np.tan(theta)

    # Define a model
    
    h_1 = 3- h_a
    
    s_a = np.ones_like(x) * 1 /1e6
    s_1 = np.ones_like(x) * sigma
    s_2 = np.ones_like(x) * sigma
    
    model_topo = np.array([h_a, h_1, s_a, s_1, s_2]).T
    model = np.array([h_1, s_1, s_2]).T
    
    dx = 8
    dz = -(h_a[8:] - h_a[:-8])
    
    alphas = np.arctan(dz/dx)
    
    src_x = x.copy()[:-8]
    src_z = (0.3 - h_a)[:-8]
    
    npos = len(h_a)
    nlay = 2
    
    depths = np.zeros((npos, nlay))
    depths[:,0] = -h_a
    depths[:,1] = -h_a - h_1
    
    rec2_x = (src_x+2) * np.cos(alphas)
    rec21_x = (src_x+2.1) * np.cos(alphas)
    rec2_z = (0.3 - h_a)[2:-6]
    
    rec4_x = (src_x+4) * np.cos(alphas)
    rec41_x = (src_x+4.1) * np.cos(alphas)
    rec4_z = (0.3 - h_a)[4:-4]
    
    rec8_x = (src_x+8) * np.cos(alphas)
    rec81_x = (src_x+8.1) * np.cos(alphas)
    rec8_z = (0.3 - h_a)[8:] 

    geom = np.array([src_x, src_z, rec2_x, rec2_z, rec4_x, rec4_z, rec8_x, rec8_z, rec21_x, rec41_x, rec81_x, alphas]).T

 #   print('geom', geom.shape)
 #   print('depths', depths.shape)
 #   print('model', model.shape)
    
    data = FDEM3D_line_topo(geom[xsrc], depths, model)

    return data


thetas = np.arange(-10,10)
thetasr = np.deg2rad(thetas)
sigmas = np.logspace(0,3)/1000

startTime = time.time()

OUT = Parallel(n_jobs=n_workers,verbose=0)(delayed(ForwardDippingTopo)(ti, si) for ti in thetasr for si in sigmas)    

endTime = time.time()

print()
print('Done in', (endTime - startTime), 'seconds!')

np.save('DippingTopo', OUT)