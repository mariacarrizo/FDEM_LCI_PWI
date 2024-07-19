import numpy as np
import matplotlib.pyplot as plt

def Plot_Datas(data_true, data_est, ax=None):
    
    if ax == None:
        fig, ax = plt.subplots(3,2, sharex=True)

    ax[0,0].semilogy(data_est[:,0,0,0], '*b', label = '2m est')
    ax[0,0].semilogy(data_est[:,0,0,1], '*r', label = '4m est')
    ax[0,0].semilogy(data_est[:,0,0,2], '*g', label = '8m est')
    ax[0,0].semilogy(data_true[:,0,0,0], ':b', label = '2m true')
    ax[0,0].semilogy(data_true[:,0,0,1], ':r', label = '4m true')
    ax[0,0].semilogy(data_true[:,0,0,2], ':g', label = '8m true')
    ax[0,0].set_title('OP component H coils')

    ax[0,1].semilogy(data_est[:,1,0,0], '*b', label = '2m est')
    ax[0,1].semilogy(data_est[:,1,0,1], '*r', label = '4m est')
    ax[0,1].semilogy(data_est[:,1,0,2], '*g', label = '8m est')
    ax[0,1].semilogy(data_true[:,1,0,0], ':b', label = '2m true')
    ax[0,1].semilogy(data_true[:,1,0,1], ':r', label = '4m true')
    ax[0,1].semilogy(data_true[:,1,0,2], ':g', label = '8m true')
    ax[0,1].set_title('IP component H coils')
    ax[0,1].legend(bbox_to_anchor=(1.1, 1.05))

    ax[1,0].semilogy(data_est[:,0,1,0], '*b', label = '2m est')
    ax[1,0].semilogy(data_est[:,0,1,1], '*r', label = '4m est')
    ax[1,0].semilogy(data_est[:,0,1,2], '*g', label = '8m est')
    ax[1,0].semilogy(data_true[:,0,1,0], ':b', label = '2m true')
    ax[1,0].semilogy(data_true[:,0,1,1], ':r', label = '4m true')
    ax[1,0].semilogy(data_true[:,0,1,2], ':g', label = '8m true')
    ax[1,0].set_title('OP component V coils')

    ax[1,1].semilogy(data_est[:,1,1,0], '*b', label = '2m est')
    ax[1,1].semilogy(data_est[:,1,1,1], '*r', label = '4m est')
    ax[1,1].semilogy(data_est[:,1,1,2], '*g', label = '8m est')
    ax[1,1].semilogy(data_true[:,1,1,0], ':b', label = '2m true')
    ax[1,1].semilogy(data_true[:,1,1,1], ':r', label = '4m true')
    ax[1,1].semilogy(data_true[:,1,1,2], ':g', label = '8m true')
    ax[1,1].set_title('IP component V coils')

    ax[2,0].semilogy(data_est[:,0,2,0], '*b', label = '2m est')
    ax[2,0].semilogy(data_est[:,0,2,1], '*r', label = '4m est')
    ax[2,0].semilogy(data_est[:,0,2,2], '*g', label = '8m est')
    ax[2,0].semilogy(data_true[:,0,2,0], ':b', label = '2m true')
    ax[2,0].semilogy(data_true[:,0,2,1], ':r', label = '4m true')
    ax[2,0].semilogy(data_true[:,0,2,2], ':g', label = '8m true')
    ax[2,0].set_title('OP component P coils')

    ax[2,1].semilogy(data_est[:,1,2,0], '*b', label = '2m est')
    ax[2,1].semilogy(data_est[:,1,2,1], '*r', label = '4m est')
    ax[2,1].semilogy(data_est[:,1,2,2], '*g', label = '8m est')
    ax[2,1].semilogy(data_true[:,1,2,0], ':b', label = '2m true')
    ax[2,1].semilogy(data_true[:,1,2,1], ':r', label = '4m true')
    ax[2,1].semilogy(data_true[:,1,2,2], ':g', label = '8m true')
    ax[2,1].set_title('IP component P coils')

    plt.tight_layout()

def grid(model, depthmax=10, ny=101, nlay=2):
    """ Generates a grid from the model to plot a 2D section
    
    I CAN IMPROVE THIS  """
    # Arrays for plotting
    npos = np.shape(model)[0] # number of 1D models
   # ny = 101 # size of the grid in y direction
    y = np.linspace(0, depthmax, ny) # y axis [m]
    grid = np.zeros((npos, ny)) # empty grid
    thk = model[:,:nlay-1].copy() # define electrical conductivities
    sig = model[:,nlay-1:].copy()  # define thicknesses
    
    # Fill the grid with the conductivity values
    
    if nlay == 3:
        for i in range(npos):
            y1 = 0
            # First layer
            while y[y1] < thk[i,0]:
                grid[i, y1] = sig[i, 0]
                y1 += 1
                #y2 = y1
            # Second layer
            while y[y1] < (thk[i,0] + thk[i,1]):
                grid[i, y1] = sig[i, 1]
                y1 += 1
            # Third layer
            grid[i, y1:] = sig[i, 2]
    
    if nlay == 2:   
        for i in range(npos):
            y1 = 0
            # First layer
            while y[y1] < thk[i,0]:
                grid[i, y1] = sig[i, 0]
                y1 += 1
            while y[y1] > thk[i,0]:
                grid[i, y1] = sig[i, 1]
                y1 += 1
        
    return grid

def Plot2Datas(data_1D, data_3D):

    fig, ax = plt.subplots(3,4, figsize=(10,5), sharex=True)
    
    # Quadrature 2m
    ax[0,0].semilogy(data_1D[:,0], '.b', label='H')
    ax[0,0].semilogy(data_3D[:,0], 'xb' )
    ax[0,0].semilogy(data_1D[:,3], '.r', label='P')
    ax[0,0].semilogy(data_3D[:,3], 'xr' )   
    ax[0,0].semilogy(data_1D[:,6], '.k', label='V')
    ax[0,0].semilogy(data_3D[:,6], 'xk' )
    ax[0,0].legend(fontsize=7)
    ax[0,0].tick_params( labelsize=7)
    ax[0,0].set_title('2m Quadrature', fontsize=7)

    ax[0,1].semilogy(100*np.abs((data_1D[:,0]-data_3D[:,0])/data_3D[:,0]), ':b', label='H2 Q')
    ax[0,1].semilogy(100*np.abs((data_1D[:,3]-data_3D[:,3])/data_3D[:,3]), ':r', label='P2 Q')
    ax[0,1].semilogy(100*np.abs((data_1D[:,6]-data_3D[:,6])/data_3D[:,6]), ':k', label='V2 Q')
    ax[0,1].legend(fontsize=7)
    ax[0,1].tick_params(labelsize=7)
    ax[0,1].set_title('2mQ Rel Diff %', fontsize=7)
    
    # Quadrature 4m
    ax[1,0].semilogy(data_1D[:,1], '.b', label = 'H4 Q')
    ax[1,0].semilogy(data_3D[:,1], 'xb')
    ax[1,0].semilogy(data_1D[:,4], '.r', label = 'P4 Q')
    ax[1,0].semilogy(data_3D[:,4], 'xr' )
    ax[1,0].semilogy(data_1D[:,7], '.k', label = 'V4 Q')
    ax[1,0].semilogy(data_3D[:,7], 'xk')
    ax[1,0].legend(fontsize=7)
    ax[1,0].tick_params( labelsize=7)
    ax[1,0].set_title('4m Quadrature', fontsize=7)

    ax[1,1].semilogy(100*np.abs((data_1D[:,1]-data_3D[:,1])/data_3D[:,1]), ':b', label='H4 Q')
    ax[1,1].semilogy(100*np.abs((data_1D[:,4]-data_3D[:,4])/data_3D[:,4]), ':r', label='P4 Q')
    ax[1,1].semilogy(100*np.abs((data_1D[:,7]-data_3D[:,7])/data_3D[:,7]), ':k', label='V4 Q')
    ax[1,1].legend(fontsize=7)
    ax[1,1].tick_params( labelsize=7)
    ax[1,1].set_title('4mQ Rel Diff %', fontsize=7)
    
    # Quadrature 8m
    ax[2,0].semilogy(data_1D[:,2], '.b', label= 'H8 Q')
    ax[2,0].semilogy(data_3D[:,2], 'xb' )
    ax[2,0].semilogy(data_1D[:,5], '.r', label= 'P8 Q')
    ax[2,0].semilogy(data_3D[:,5], 'xr')
    ax[2,0].semilogy(data_1D[:,8], '.k', label= 'V8 Q')
    ax[2,0].semilogy(data_3D[:,8], 'xk' )
    ax[2,0].legend(fontsize=7)
    ax[2,0].tick_params( labelsize=7)
    ax[2,0].set_title('8m Quadrature', fontsize=7)

    ax[2,1].semilogy(100*np.abs((data_1D[:,2]-data_3D[:,2])/data_3D[:,2]), ':b', label='H8 Q')
    ax[2,1].semilogy(100*np.abs((data_1D[:,5]-data_3D[:,5])/data_3D[:,5]), ':r', label='P8 Q')
    ax[2,1].semilogy(100*np.abs((data_1D[:,8]-data_3D[:,8])/data_3D[:,8]), ':k', label='V8 Q')
    ax[2,1].legend(fontsize=7)
    ax[2,1].tick_params(labelsize=7)
    ax[2,1].set_title('8mQ Rel Diff %', fontsize=7)
    
    # In-Phase 2m
    ax[0,2].semilogy(data_1D[:,9], '.b', label='H2 IP')
    ax[0,2].semilogy(data_3D[:,9], 'xb' )
    ax[0,2].semilogy(data_1D[:,12], '.r', label='P2 IP')
    ax[0,2].semilogy(data_3D[:,12], 'xr' )
    ax[0,2].semilogy(data_1D[:,15], '.k', label='V2 IP')
    ax[0,2].semilogy(data_3D[:,15], 'xk' )
    ax[0,2].legend(fontsize=7)
    ax[0,2].tick_params( labelsize=7)
    ax[0,2].set_title('2m In-Phase', fontsize=7)

    ax[0,3].semilogy(100*np.abs((data_1D[:,9]-data_3D[:,9])/data_3D[:,9]), ':b', label = 'H2 IP')
    ax[0,3].semilogy(100*np.abs((data_1D[:,12]-data_3D[:,12])/data_3D[:,12]), ':r', label = 'P2 IP')
    ax[0,3].semilogy(100*np.abs((data_1D[:,15]-data_3D[:,15])/data_3D[:,15]), ':k', label='V2 IP')
    ax[0,3].legend(fontsize=7)
    ax[0,3].tick_params(labelsize=7)
    ax[0,3].set_title('2mIP Rel Diff %', fontsize=7)
    
    # In-Phase 4m
    ax[1,2].semilogy(data_1D[:,10], '.b', label = 'H4 IP')
    ax[1,2].semilogy(data_3D[:,10], 'xb' )
    ax[1,2].semilogy(data_1D[:,13], '.r', label = 'P4 IP')
    ax[1,2].semilogy(data_3D[:,13], 'xr' )
    ax[1,2].semilogy(data_1D[:,16], '.k', label = 'V4 IP')
    ax[1,2].semilogy(data_3D[:,16], 'xk' )
    ax[1,2].legend(fontsize=7)
    ax[1,2].tick_params(labelsize=7)
    ax[1,2].set_title('4m In-Phase', fontsize=7)
    
    ax[1,3].semilogy(100*np.abs((data_1D[:,10]-data_3D[:,10])/data_3D[:,10]), ':b', label = 'H4 IP')
    ax[1,3].semilogy(100*np.abs((data_1D[:,13]-data_3D[:,13])/data_3D[:,13]), ':r', label = 'P4 IP')
    ax[1,3].semilogy(100*np.abs((data_1D[:,16]-data_3D[:,16])/data_3D[:,16]), ':k', label='V4 IP')
    ax[1,3].legend(fontsize=7)
    ax[1,3].tick_params(labelsize=7)
    ax[1,3].set_title('4mIP Rel Diff %', fontsize=7)
    
    # In-Phase 8m
    ax[2,2].semilogy(data_1D[:,11], '.b', label= 'H8 IP')
    ax[2,2].semilogy(data_3D[:,11], 'xb' )
    ax[2,2].semilogy(data_1D[:,14], '.r', label= 'P8 IP')
    ax[2,2].semilogy(data_3D[:,14], 'xr' )
    ax[2,2].semilogy(data_1D[:,17], '.k', label= 'V8 IP')
    ax[2,2].semilogy(data_3D[:,17], 'xk' )
    ax[2,2].legend(fontsize=7)
    ax[2,2].tick_params(labelsize=7)
    ax[2,2].set_title('8m In-Phase', fontsize=7)

    ax[2,3].semilogy(100*np.abs((data_1D[:,11]-data_3D[:,11])/data_3D[:,11]), ':b', label = 'H8 IP')
    ax[2,3].semilogy(100*np.abs((data_1D[:,14]-data_3D[:,14])/data_3D[:,14]), ':r', label = 'P8 IP')
    ax[2,3].semilogy(100*np.abs((data_1D[:,17]-data_3D[:,17])/data_3D[:,17]), ':k', label='V8 IP')
    ax[2,3].legend(fontsize=7)
    ax[2,3].tick_params(labelsize=7)
    ax[2,3].set_title('8mIP Rel Diff %', fontsize=7)
    
    plt.tight_layout()
    
def grid(model, depthmax=8, ny=101, nlay=2):
    """ Generates a grid from the model to plot a 2D section
    """
    # Arrays for plotting
    npos = np.shape(model)[0] # number of 1D models
   # ny = 101 # size of the grid in y direction
    y = np.linspace(0, depthmax, ny) # y axis [m]
    grid = np.zeros((npos, ny)) # empty grid
    thk = model[:,:nlay-1].copy() # define electrical conductivities
    sig = model[:,nlay-1:].copy()  # define thicknesses
    
    # Fill the grid with the conductivity values
    
    if nlay == 3:
        for i in range(npos):
            y1 = 0
            # First layer
            while y[y1] < thk[i,0]:
                grid[i, y1] = sig[i, 0]
                y1 += 1
                if y1 > ny-1:
                    break
                #y2 = y1
            # Second layer
            while y[y1] < (thk[i,0] + thk[i,1]):
                grid[i, y1] = sig[i, 1]
                y1 += 1
                if y1 > ny-1:
                    break
            # Third layer
            grid[i, y1:] = sig[i, 2]
    
    if nlay == 2:   
        for i in range(npos):
            y1 = 0
            # First layer
            while y[y1] < thk[i,0]:
                grid[i, y1] = sig[i, 0]
                y1 += 1
                if y1 > ny-1:
                    break
            while y[y1] >= thk[i,0]:
                grid[i, y1] = sig[i, 1]
                y1 += 1
                if y1 > ny-1:
                    break
        
    return grid
    

