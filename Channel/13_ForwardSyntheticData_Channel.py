# Script to create synthetic 3D data

import numpy as np
import emg3d 
#import empymod as ep
import pandas as pd
from scipy.constants import mu_0
#import matplotlib.pyplot as plt
import time
from joblib import Parallel, delayed
import sys
sys.path.insert(1, 'src')


# 0. Define instrument settings

height = 0.15
frequency = 9000
n_workers = 40

# 2. Define source positions

src_x = np.arange(0,40,1)
src_y = np.arange(0,40,1)
src = np.meshgrid(src_x, src_y)

x = src[0].ravel()
y = src[1].ravel()

src_list = np.array([x, y]).T

# 3. Define a model

# In XY direction

x = np.linspace(-10, 50, 60)
y = np.linspace(-10, 50, 60)

xx = np.linspace(-10, 50, 60)
yy = np.linspace(-10, 50, 60)

X, Y = np.meshgrid(x, y) 

def cxy(x,y):

    ci = []
    
    xx = np.hstack(x)
    yy = np.hstack(y)

    for xi,yi in zip(xx,yy):

        if ((yi-3)**3 >= (xi-40)**2) and ((yi-20)**3 < (xi-40)**2):
            ci.append(1)

        elif ((yi-3)**3 <= (xi-40)**2) and ((yi)**3 >= (xi-40)**2):
            ci.append(3)

        elif ((yi-20)**3 > (xi-40)**2)and ((yi-25)**3 < (xi-40)**2):
            ci.append(4)
        else:
            ci.append(2)

    c = np.array(ci).reshape(np.shape(x))
    return c

cxy = cxy(X,Y)

# Create 2 layered models

cxy = cxy.T
s_p = 10/1000 # Values of conductivity
s_g = 100/1000
s_c = 50/1000
s_f = 30/1000

slope1 = 1/3
slope2 = -1/5

b1 = -1.2
b2 = +8

m = []

for i in range(cxy.shape[0]):
    for j in range(cxy.shape[1]):
        if cxy[i,j] == 1: # channel
            h = 3
            s1 = s_c
            s2 = s_g
            m.append([h, s1, s2])
        if cxy[i,j] == 2: # plain
            h = 2
            s1 = s_p
            s2 = s_g
            m.append([h, s1, s2])
        if cxy[i,j] == 3: # bars
            h = 2.5 # slope1 * Y[i,j] + b1
            s1 = s_f
            s2 = s_g
            m.append([h, s1, s2])
        if cxy[i,j] == 4: # bars
            h = 2.5 #slope2 * Y[i,j] + b2
            s1 = s_f
            s2 = s_g
            m.append([h, s1, s2])

# model
m = np.array(m).reshape(60,60,3)

# model with air layer

depths_air = m[:,:,0].copy() * 0
depths = np.stack((depths_air, -m[:,:,0]), axis=2)

sigmas_1 = m[:,:,1]
sigmas_2 = m[:,:,2]

# 2. Create a mesh

# Define a homogoneous model
sig = np.array([100/1000])
thk = np.array([])

# Insert air layer
sig_3d = np.hstack(([1/1e6], sig))
depth_3d = np.hstack(([0], -np.cumsum(thk)))


def ForwardChannel(src_x, src_y):

    # mesh
    mesh = emg3d.construct_mesh(frequency = frequency,
                             properties = [20/1000, 20/1000, sig_3d[0]],
                             center = [src_x, src_y, height],
                             mapping='Conductivity',
                             domain = ([src_x-10, src_x+20],[src_y-10, src_y+10],[-10,10]),
                             min_width_limits = [0.2, 0.2, 0.1], # changed z from 0.1 to 0.2
                             center_on_edge=False,
                             stretching= {'x': [1,1.5], 'y': [1.1,1.5], 'z': [1,1.5]}, 
                             lambda_from_center=True,
                             lambda_factor=3, 
                             )

    print(mesh)
    # 3. Populate mesh
    
    # Define air layer
    sig_x = np.ones(mesh.n_cells)*sig_3d[0] # empty array to be populated
    sig_air = np.ones(mesh.n_cells)*sig_3d[0] # air array

    # Fill y-axis for y < 0
    
    x = np.ones_like(mesh.cell_centers[:,0], dtype=bool)  
    y = np.ones_like(mesh.cell_centers[:,1], dtype=bool) 
    z_lay1 = (mesh.cell_centers[:,2] < depths[0,0,0]) & (mesh.cell_centers[:,2] > depths[0,0,1])
    z_lay2 = (mesh.cell_centers[:,2] < depths[0,0,1]) 
    
    sig_x[x*y*z_lay1] = m[0,0,1] # First layer sigma
    sig_x[x*y*z_lay2] = m[0,0,2] # Second layer sigma
    
    # Fill internal positions
    
    for i in range(len(xx)-1):
        for j in range(len(yy)-1):
       
            x = (mesh.cell_centers[:,0] >= xx[i]) & (mesh.cell_centers[:,0] < xx[i+1])
            y = (mesh.cell_centers[:,1] >= yy[j]) & (mesh.cell_centers[:,1] < yy[j+1])
            z_lay1 = (mesh.cell_centers[:,2] < depths[i,j,0]) & (mesh.cell_centers[:,2] > depths[i,j,1])
            z_lay2 = (mesh.cell_centers[:,2] < depths[i,j,1]) 
        
            sig_x[x*y*z_lay1] = m[i,j,1]
            sig_x[x*y*z_lay2] = m[i,j,2]
    
    #  4. Define models
    
    Model = emg3d.Model(mesh, 
                     property_x = sig_x,
                     mapping = 'Conductivity')
    
    Model_air = emg3d.Model(mesh,
                         property_x = sig_air,
                         mapping = 'Conductivity')

    #mesh.plot_3d_slicer(Model.property_x, zslice=-2, xlim=[-20,60], ylim = [-20,60], zlim=[-6,2], )
    
    print('Defining geometry')
    # Define source coordinates
    
    Hsrc_coords = [src_x, src_y, height, 0, 90]
    Vsrc_coords = [src_x, src_y, height, 90, 0]
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
    H_Hrec = Hfield_H.get_receiver((offsets_HV, np.ones_like(offsets_HV)*src_y, height, 0, 90))*(2j * np.pi * frequency * mu_0) 
    # For primary field Hsource
    H_Hrec_p = Hfield_H_p.get_receiver((offsets_HV, np.ones_like(offsets_HV)*src_y, height, 0, 90))*(2j * np.pi * frequency * mu_0) 
    # Secondary field Hsource
    H_Hrec_s = H_Hrec - H_Hrec_p
    
    # For total field Vsource
    H_Vrec = Hfield_V.get_receiver((offsets_HV, np.ones_like(offsets_HV)*src_y, height, 90, 0))*(2j * np.pi * frequency * mu_0) 
    # For primary field Vsource
    H_Vrec_p = Hfield_V_p.get_receiver((offsets_HV, np.ones_like(offsets_HV)*src_y, height, 90, 0))*(2j * np.pi * frequency * mu_0) 
    # Secondary field Vsource
    H_Vrec_s = H_Vrec - H_Vrec_p
    
    # For total field Psource
    H_Prec = Hfield_H.get_receiver((offsets_P, np.ones_like(offsets_P)*src_y, height, 0, 0))*(2j * np.pi * frequency * mu_0) 
    # For primary field Psource in xz direction
    H_Prec_p_xz = Hfield_H_p.get_receiver((offsets_P, np.ones_like(offsets_P)*src_y, height, 0, 0))*(2j * np.pi * frequency * mu_0) 
    # Secondary field Psource
    H_Prec_s = H_Prec - H_Prec_p_xz
    # Primary field Psource in zz direction
    H_Prec_p = Hfield_H_p.get_receiver((offsets_P, np.ones_like(offsets_P)*src_y, height, 0, 90))*(2j * np.pi * frequency * mu_0)
    
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
    
    OUT_i = pd.DataFrame({'geom'  : ['H2', 'H4', 'H8', 'V2', 'V4', 'V8', 'P2', 'P4', 'P8'],
                          'src_x' : [Hsrc_coords[0], Hsrc_coords[0], Hsrc_coords[0],
                                     Vsrc_coords[0], Vsrc_coords[0], Vsrc_coords[0],
                                     Hsrc_coords[0], Hsrc_coords[0], Hsrc_coords[0]],
                          'src_y' : [Hsrc_coords[1], Hsrc_coords[1], Hsrc_coords[1],
                                     Vsrc_coords[1], Vsrc_coords[1], Vsrc_coords[1],
                                     Hsrc_coords[1], Hsrc_coords[1], Hsrc_coords[1]],
                          'rec_x' : np.hstack((offsets_HV, offsets_HV, offsets_P)),
                          'rec_y' : [Hsrc_coords[1], Hsrc_coords[1], Hsrc_coords[1],
                                     Vsrc_coords[1], Vsrc_coords[1], Vsrc_coords[1],
                                     Hsrc_coords[1], Hsrc_coords[1], Hsrc_coords[1]],
                          'midpx' : np.hstack((Hsrc_coords[0] + (offsets_HV - Hsrc_coords[0])/2,
                                               Vsrc_coords[0] + (offsets_HV - Vsrc_coords[0])/2,
                                               Hsrc_coords[0] + (offsets_P - Hsrc_coords[0])/2)),
                          'op'    : np.hstack((op_h, op_v, op_p)),
                          'ip'    : np.hstack((ip_h, ip_v, ip_p)) 
                          })
    
    #OUT = pd.concat([OUT, OUT_i], ignore_index=True)
    print()
    return OUT_i

startTime = time.time()
                 
OUT = Parallel(n_jobs=n_workers, verbose=0)(delayed(ForwardChannel)(src[0], src[1]) for src in src_list)

#print(OUT)
                 
print()
endTime = time.time()
print('Done in', (endTime - startTime), 'seconds!')

OUT_dataframe = pd.concat(OUT)

#np.save('data/data_s1_c1_uc', OUT)
OUT_dataframe.to_pickle('data/data_3DChannel.pkl')
