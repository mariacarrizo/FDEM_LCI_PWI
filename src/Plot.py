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

def grid(model, depthmax=10, ny=101):
    """ Generates a grid from the model to plot a 2D section"""
    # Arrays for plotting
    npos = np.shape(model)[0] # number of 1D models
   # ny = 101 # size of the grid in y direction
    y = np.linspace(0, depthmax, ny) # y axis [m]
    grid = np.zeros((npos, ny)) # empty grid
    thk = model[:,:2].copy() # define electrical conductivities
    sig = model[:,2:].copy()  # define thicknesses
    
    # Fill the grid with the conductivity values
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
        
    return grid