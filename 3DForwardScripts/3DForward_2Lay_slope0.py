import numpy as np
import emg3d 
#import empymod as ep
import pandas as pd
from scipy.constants import mu_0
import time
import sys
sys.path.insert(1, 'src')
from Plot import grid

# Define a homogoneous model
sig = np.array([100/1000])
thk = np.array([])

sig_3d = np.hstack(([1/1e6], sig))
depth_3d = np.hstack(([0], -np.cumsum(thk)))

# Instrument settings
height = 0.1
frequency = 9000

# Define mesh
mesh = emg3d.construct_mesh(frequency = frequency,
                         properties = sig_3d,
                         center = [0.25,0.25,0],
                         mapping='Conductivity',
                         domain = ([-10, 40],[-6, 6],[-13,1]),
                         min_width_limits = [0.5, 0.5, 0.1],
                         center_on_edge=True)

# Load LCI model
models_LCI = np.load('modelLCI_slope0.npy')

npos = np.shape(models_LCI)[0]
nlay = int((np.shape(models_LCI)[1]+1)/2)

depths = np.zeros((npos, nlay))
depths[:,1] = - models_LCI[:,0]

#models_LCI_grid = grid(models_LCI, depthmax = 10)

# Populate a mesh
# Define air layer
sig_x = np.ones(mesh.n_cells)*sig_3d[0]
sig_air = np.ones(mesh.n_cells)*sig_3d[0]

# Fill before position 0
x = mesh.cell_centers[:,0] <=0
y = np.ones_like(mesh.cell_centers[:,1], dtype=bool)
z_lay1 = (mesh.cell_centers[:,2] < depths[0,0]) & (mesh.cell_centers[:,2] > depths[0,1])
z_lay2 = (mesh.cell_centers[:,2] < depths[0,1]) 

sig_x[x*y*z_lay1] = models_LCI[0,1]
sig_x[x*y*z_lay2] = models_LCI[0,2]

for p in range(npos):
    x = (mesh.cell_centers[:,0] > p) & (mesh.cell_centers[:,0] < p+1)
    y = np.ones_like(mesh.cell_centers[:,1], dtype=bool)
    z_lay1 = (mesh.cell_centers[:,2] < depths[p,0]) & (mesh.cell_centers[:,2] > depths[p,1])
    z_lay2 = (mesh.cell_centers[:,2] < depths[p,1]) 

    sig_x[x*y*z_lay1] = models_LCI[p,1]
    sig_x[x*y*z_lay2] = models_LCI[p,2]

# fill after position npos
x = (mesh.cell_centers[:,0] > npos) 
y = np.ones_like(mesh.cell_centers[:,1], dtype=bool)
z_lay1 = (mesh.cell_centers[:,2] < depths[-1,0]) & (mesh.cell_centers[:,2] > depths[-1,1])
z_lay2 = (mesh.cell_centers[:,2] < depths[-1,1]) 

sig_x[x*y*z_lay1] = models_LCI[-1,1]
sig_x[x*y*z_lay2] = models_LCI[-1,2]

# Create 3D model
Model_LCI = emg3d.Model(mesh, property_x = sig_x, mapping = 'Conductivity')
Model_air = emg3d.Model(mesh, property_x = sig_air, mapping = 'Conductivity')

# Start computing data

# Set the source positions to obtain full coverage midpoints in each 1D model
# 4 positions before and 3 positions after have no coverage
xsrc = np.linspace(-4, npos+3, npos+8, endpoint=True)
print('xsrc:', xsrc)
print()

# Empty data array
OUT = pd.DataFrame({})

startTime = time.time()
for p in range(npos+5):
    print('Position:', p)
    print('Defining geometry')
    # Define source coordinates
    src_x = xsrc[p]
    Hsrc_coords = [src_x, 0, height, 0, 90]
    Vsrc_coords = [src_x, 0, height, 90, 0]
    print('source:', Hsrc_coords)
    
    # Define H and V receivers coordinates
    offsets_HV = np.array([xsrc[p]+2, xsrc[p]+4, xsrc[p]+8])
    print('offsets:',offsets_HV)
    
    # Define P receivers coordinates
    offsets_P = np.array([xsrc[p]+2.1, xsrc[p]+4.1, xsrc[p]+8.1])
    
    # Define sources
    Hsource = emg3d.TxMagneticPoint(Hsrc_coords)
    Vsource = emg3d.TxMagneticPoint(Vsrc_coords)
    
    # Solve Electrical fields
    print('Solving sources...')
    # Total field Hsource
    Efield_H = emg3d.solve_source(model = Model_LCI, source = Hsource, frequency = frequency)
    # Primary field Hsource
    Efield_H_p = emg3d.solve_source(model = Model_air, source = Hsource, frequency = frequency)
    
    # Total field Vsource
    Efield_V = emg3d.solve_source(model = Model_LCI, source = Vsource, frequency = frequency)
    # Primary field Vsource
    Efield_V_p = emg3d.solve_source(model = Model_air, source = Vsource, frequency = frequency)

    # Get magnetic fields
    print('getting magnetic fields...')
    # Total magnetic field Hsource
    Hfield_H = emg3d.get_magnetic_field(model = Model_LCI, efield = Efield_H)
    # Primary magnetic field Hsource
    Hfield_H_p = emg3d.get_magnetic_field(model = Model_air, efield = Efield_H_p)
    
    # Total magnetic field Vsource
    Hfield_V = emg3d.get_magnetic_field(model = Model_LCI, efield = Efield_V)
    # Primary magnetic field Vsource
    Hfield_V_p = emg3d.get_magnetic_field(model = Model_air, efield = Efield_V_p)
    
    # Get fields at receivers
    print('magnetic field at receivers...')
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
    print('getting output components')
    # Horizontal coplanar
    op_h = (H_Hrec_s/H_Hrec_p).imag.amp()
    ip_h = (H_Hrec_s/H_Hrec_p).real.amp()
    
    # Vertical coplanar
    op_v = (H_Vrec_s/H_Vrec_p).imag.amp()
    ip_v = (H_Vrec_s/H_Vrec_p).real.amp()
    
    # Perpendicular
    op_p = (H_Prec_s/H_Prec_p).imag.amp()
    ip_p = (H_Prec_s/H_Prec_p).real.amp()
        
    OUT_i = pd.DataFrame({'geom'  : ['H2', 'H4', 'H8', 'V2', 'V4', 'V8', 'P2', 'P4', 'P8'],
                          'src_x' : [Hsrc_coords[0], Hsrc_coords[0], Hsrc_coords[0],
                                     Vsrc_coords[0], Vsrc_coords[0], Vsrc_coords[0],
                                     Hsrc_coords[0], Hsrc_coords[0], Hsrc_coords[0]],
                          'rec_x' : np.hstack((offsets_HV, offsets_HV, offsets_P)),
                          'midpx' : np.hstack((Hsrc_coords[0] + (offsets_HV - Hsrc_coords[0])/2,
                                               Vsrc_coords[0] + (offsets_HV - Vsrc_coords[0])/2,
                                               Hsrc_coords[0] + (offsets_P - Hsrc_coords[0])/2)),
                          'offset': [2, 4, 8, 2, 4, 8, 2.1, 4.1, 8.1],
                          'op'    : np.hstack((op_h, op_v, op_p)),
                          'ip'    : np.hstack((ip_h, ip_v, ip_p)) 
                          })
    
    OUT = pd.concat([OUT, OUT_i], ignore_index=True)
    print()
endTime = time.time()
print('Done in', (endTime - startTime)/2, 'minutes!')

OUT.to_pickle('data3D_slope0.pkl')
