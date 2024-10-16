# Script to create the synthetic models

import numpy as np

# number of positions (number of soundings)
pos = 40

# number of layers
nLayers = 2

# Distance vector X assuming 1 sounding per meter
x =  np.linspace(0,pos,pos, endpoint=False)

# Model array
model_s0_c1_uc = np.zeros((pos, nLayers*2-1))
model_s0_c2_uc = np.zeros((pos, nLayers*2-1))
model_s0_c3_uc = np.zeros((pos, nLayers*2-1))
model_s0_c4_uc = np.zeros((pos, nLayers*2-1))

model_s1_c1_uc = np.zeros((pos, nLayers*2-1)) # slope 1% contrast 1 order - upper conductive
model_s2_c1_uc = np.zeros((pos, nLayers*2-1)) 
model_s5_c1_uc = np.zeros((pos, nLayers*2-1))
model_s10_c1_uc = np.zeros((pos, nLayers*2-1))

model_s1_c2_uc = np.zeros((pos, nLayers*2-1)) # slope 1% contrast 2 order
model_s2_c2_uc = np.zeros((pos, nLayers*2-1)) 
model_s5_c2_uc = np.zeros((pos, nLayers*2-1))
model_s10_c2_uc = np.zeros((pos, nLayers*2-1))

model_s1_c3_uc = np.zeros((pos, nLayers*2-1)) # slope 1% contrast 3 order
model_s2_c3_uc = np.zeros((pos, nLayers*2-1)) 
model_s5_c3_uc = np.zeros((pos, nLayers*2-1))
model_s10_c3_uc = np.zeros((pos, nLayers*2-1))

model_s1_c4_uc = np.zeros((pos, nLayers*2-1)) # slope 1% contrast 4 order
model_s2_c4_uc = np.zeros((pos, nLayers*2-1)) 
model_s5_c4_uc = np.zeros((pos, nLayers*2-1))
model_s10_c4_uc = np.zeros((pos, nLayers*2-1))

model_s1_c1_ur = np.zeros((pos, nLayers*2-1)) # slope 1% contrast 1 order - upper resistive
model_s2_c1_ur = np.zeros((pos, nLayers*2-1)) 
model_s5_c1_ur = np.zeros((pos, nLayers*2-1))
model_s10_c1_ur = np.zeros((pos, nLayers*2-1))

model_s1_c2_ur = np.zeros((pos, nLayers*2-1)) # slope 1% contrast 2 order
model_s2_c2_ur = np.zeros((pos, nLayers*2-1)) 
model_s5_c2_ur = np.zeros((pos, nLayers*2-1))
model_s10_c2_ur = np.zeros((pos, nLayers*2-1))

model_s1_c3_ur = np.zeros((pos, nLayers*2-1)) # slope 1% contrast 3 order
model_s2_c3_ur = np.zeros((pos, nLayers*2-1)) 
model_s5_c3_ur = np.zeros((pos, nLayers*2-1))
model_s10_c3_ur = np.zeros((pos, nLayers*2-1))

model_s1_c4_ur = np.zeros((pos, nLayers*2-1)) # slope 1% contrast 4 order
model_s2_c4_ur = np.zeros((pos, nLayers*2-1)) 
model_s5_c4_ur = np.zeros((pos, nLayers*2-1))
model_s10_c4_ur = np.zeros((pos, nLayers*2-1))

# Including electrical conductivities in the model array [S/m]
model_s1_c1_ur[:,1] = 20/1000    # First layer
model_s1_c1_ur[:,2] = 200/1000   # Second layer
model_s2_c1_ur[:,1] = 20/1000
model_s2_c1_ur[:,2] = 200/1000
model_s5_c1_ur[:,1] = 20/1000
model_s5_c1_ur[:,2] = 200/1000
model_s10_c1_ur[:,1] = 20/1000
model_s10_c1_ur[:,2] = 200/1000

model_s1_c2_ur[:,1] = 20/1000    # First layer
model_s1_c2_ur[:,2] = 400/1000   # Second layer
model_s2_c2_ur[:,1] = 20/1000
model_s2_c2_ur[:,2] = 400/1000
model_s5_c2_ur[:,1] = 20/1000
model_s5_c2_ur[:,2] = 400/1000
model_s10_c2_ur[:,1] = 20/1000
model_s10_c2_ur[:,2] = 400/1000

model_s1_c3_ur[:,1] = 20/1000    # First layer
model_s1_c3_ur[:,2] = 800/1000   # Second layer
model_s2_c3_ur[:,1] = 20/1000
model_s2_c3_ur[:,2] = 800/1000
model_s5_c3_ur[:,1] = 20/1000
model_s5_c3_ur[:,2] = 800/1000
model_s10_c3_ur[:,1] = 20/1000
model_s10_c3_ur[:,2] = 800/1000

model_s1_c4_ur[:,1] = 20/1000    # First layer
model_s1_c4_ur[:,2] = 1600/1000   # Second layer
model_s2_c4_ur[:,1] = 20/1000
model_s2_c4_ur[:,2] = 1600/1000
model_s5_c4_ur[:,1] = 20/1000
model_s5_c4_ur[:,2] = 1600/1000
model_s10_c4_ur[:,1] = 20/1000
model_s10_c4_ur[:,2] = 1600/1000

model_s0_c1_uc[:,1] = 200/1000
model_s0_c1_uc[:,2] = 20/1000
model_s1_c1_uc[:,1] = 200/1000    # First layer
model_s1_c1_uc[:,2] = 20/1000   # Second layer
model_s2_c1_uc[:,1] = 200/1000
model_s2_c1_uc[:,2] = 20/1000
model_s5_c1_uc[:,1] = 200/1000
model_s5_c1_uc[:,2] = 20/1000
model_s10_c1_uc[:,1] = 200/1000
model_s10_c1_uc[:,2] = 20/1000

model_s0_c2_uc[:,1] = 400/1000
model_s0_c2_uc[:,2] = 20/1000
model_s1_c2_uc[:,1] = 400/1000    # First layer
model_s1_c2_uc[:,2] = 20/1000   # Second layer
model_s2_c2_uc[:,1] = 400/1000
model_s2_c2_uc[:,2] = 20/1000
model_s5_c2_uc[:,1] = 400/1000
model_s5_c2_uc[:,2] = 20/1000
model_s10_c2_uc[:,1] = 400/1000
model_s10_c2_uc[:,2] = 20/1000

model_s0_c3_uc[:,1] = 800/1000
model_s0_c3_uc[:,2] = 20/1000
model_s1_c3_uc[:,1] = 800/1000    # First layer
model_s1_c3_uc[:,2] = 20/1000   # Second layer
model_s2_c3_uc[:,1] = 800/1000
model_s2_c3_uc[:,2] = 20/1000
model_s5_c3_uc[:,1] = 800/1000
model_s5_c3_uc[:,2] = 20/1000
model_s10_c3_uc[:,1] = 800/1000
model_s10_c3_uc[:,2] = 20/1000

model_s0_c4_uc[:,1] = 1600/1000
model_s0_c4_uc[:,2] = 20/1000
model_s1_c4_uc[:,1] = 1600/1000    # First layer
model_s1_c4_uc[:,2] = 20/1000   # Second layer
model_s2_c4_uc[:,1] = 1600/1000
model_s2_c4_uc[:,2] = 20/1000
model_s5_c4_uc[:,1] = 1600/1000
model_s5_c4_uc[:,2] = 20/1000
model_s10_c4_uc[:,1] = 1600/1000
model_s10_c4_uc[:,2] = 20/1000

# Thickness of the first layer
y1 = 2.5 # thickness of middle point
x0 = 0 # x position of start slope
x1 = 10 # x position middle of slope
x2 = 30 # x position end of slope

# Slope 1 %
slope = 1/100
intercept = y1 - slope*(x1 - x0)
thk_s1 = intercept + slope * x

model_s1_c1_uc[:,0] = thk_s1
model_s1_c1_uc[:x1,0] = thk_s1[x1]
model_s1_c1_uc[x2:,0] = thk_s1[x2]

model_s1_c2_uc[:,0] = thk_s1
model_s1_c2_uc[:x1,0] = thk_s1[x1]
model_s1_c2_uc[x2:,0] = thk_s1[x2]

model_s1_c3_uc[:,0] = thk_s1
model_s1_c3_uc[:x1,0] = thk_s1[x1]
model_s1_c3_uc[x2:,0] = thk_s1[x2]

model_s1_c4_uc[:,0] = thk_s1
model_s1_c4_uc[:x1,0] = thk_s1[x1]
model_s1_c4_uc[x2:,0] = thk_s1[x2]

model_s1_c1_ur[:,0] = thk_s1
model_s1_c1_ur[:x1,0] = thk_s1[x1]
model_s1_c1_ur[x2:,0] = thk_s1[x2]

model_s1_c2_ur[:,0] = thk_s1
model_s1_c2_ur[:x1,0] = thk_s1[x1]
model_s1_c2_ur[x2:,0] = thk_s1[x2]

model_s1_c3_ur[:,0] = thk_s1
model_s1_c3_ur[:x1,0] = thk_s1[x1]
model_s1_c3_ur[x2:,0] = thk_s1[x2]

model_s1_c4_ur[:,0] = thk_s1
model_s1_c4_ur[:x1,0] = thk_s1[x1]
model_s1_c4_ur[x2:,0] = thk_s1[x2]

# Slope 2 %
slope = 2/100
intercept = y1 - slope*(x1 - x0)
thk_s2 = intercept + slope * x

model_s2_c1_uc[:,0] = thk_s2
model_s2_c1_uc[:x1,0] = thk_s2[x1]
model_s2_c1_uc[x2:,0] = thk_s2[x2]

model_s2_c2_uc[:,0] = thk_s2
model_s2_c2_uc[:x1,0] = thk_s2[x1]
model_s2_c2_uc[x2:,0] = thk_s2[x2]

model_s2_c3_uc[:,0] = thk_s2
model_s2_c3_uc[:x1,0] = thk_s2[x1]
model_s2_c3_uc[x2:,0] = thk_s2[x2]

model_s2_c4_uc[:,0] = thk_s2
model_s2_c4_uc[:x1,0] = thk_s2[x1]
model_s2_c4_uc[x2:,0] = thk_s2[x2]

model_s2_c1_ur[:,0] = thk_s2
model_s2_c1_ur[:x1,0] = thk_s2[x1]
model_s2_c1_ur[x2:,0] = thk_s2[x2]

model_s2_c2_ur[:,0] = thk_s2
model_s2_c2_ur[:x1,0] = thk_s2[x1]
model_s2_c2_ur[x2:,0] = thk_s2[x2]

model_s2_c3_ur[:,0] = thk_s2
model_s2_c3_ur[:x1,0] = thk_s2[x1]
model_s2_c3_ur[x2:,0] = thk_s2[x2]

model_s2_c4_ur[:,0] = thk_s2
model_s2_c4_ur[:x1,0] = thk_s2[x1]
model_s2_c4_ur[x2:,0] = thk_s2[x2]

# Slope 5 %
slope = 5/100
intercept = y1 - slope*(x1 - x0)
thk_s5 = intercept + slope * x

model_s5_c1_uc[:,0] = thk_s5
model_s5_c1_uc[:x1,0] = thk_s5[x1]
model_s5_c1_uc[x2:,0] = thk_s5[x2]

model_s5_c2_uc[:,0] = thk_s5
model_s5_c2_uc[:x1,0] = thk_s5[x1]
model_s5_c2_uc[x2:,0] = thk_s5[x2]

model_s5_c3_uc[:,0] = thk_s5
model_s5_c3_uc[:x1,0] = thk_s5[x1]
model_s5_c3_uc[x2:,0] = thk_s5[x2]

model_s5_c4_uc[:,0] = thk_s5
model_s5_c4_uc[:x1,0] = thk_s5[x1]
model_s5_c4_uc[x2:,0] = thk_s5[x2]

model_s5_c1_ur[:,0] = thk_s5
model_s5_c1_ur[:x1,0] = thk_s5[x1]
model_s5_c1_ur[x2:,0] = thk_s5[x2]

model_s5_c2_ur[:,0] = thk_s5
model_s5_c2_ur[:x1,0] = thk_s5[x1]
model_s5_c2_ur[x2:,0] = thk_s5[x2]

model_s5_c3_ur[:,0] = thk_s5
model_s5_c3_ur[:x1,0] = thk_s5[x1]
model_s5_c3_ur[x2:,0] = thk_s5[x2]

model_s5_c4_ur[:,0] = thk_s5
model_s5_c4_ur[:x1,0] = thk_s5[x1]
model_s5_c4_ur[x2:,0] = thk_s5[x2]

# Slope 10 %
slope = 10/100
intercept = y1 - slope*(x1 - x0)
thk_s10 = intercept + slope * x

model_s10_c1_uc[:,0] = thk_s10
model_s10_c1_uc[:x1,0] = thk_s10[x1]
model_s10_c1_uc[x2:,0] = thk_s10[x2]

model_s10_c2_uc[:,0] = thk_s10
model_s10_c2_uc[:x1,0] = thk_s10[x1]
model_s10_c2_uc[x2:,0] = thk_s10[x2]

model_s10_c3_uc[:,0] = thk_s10
model_s10_c3_uc[:x1,0] = thk_s10[x1]
model_s10_c3_uc[x2:,0] = thk_s10[x2]

model_s10_c4_uc[:,0] = thk_s10
model_s10_c4_uc[:x1,0] = thk_s10[x1]
model_s10_c4_uc[x2:,0] = thk_s10[x2]

model_s10_c1_ur[:,0] = thk_s10
model_s10_c1_ur[:x1,0] = thk_s10[x1]
model_s10_c1_ur[x2:,0] = thk_s10[x2]

model_s10_c2_ur[:,0] = thk_s10
model_s10_c2_ur[:x1,0] = thk_s10[x1]
model_s10_c2_ur[x2:,0] = thk_s10[x2]

model_s10_c3_ur[:,0] = thk_s10
model_s10_c3_ur[:x1,0] = thk_s10[x1]
model_s10_c3_ur[x2:,0] = thk_s10[x2]

model_s10_c4_ur[:,0] = thk_s10
model_s10_c4_ur[:x1,0] = thk_s10[x1]
model_s10_c4_ur[x2:,0] = thk_s10[x2]

# Include thickness in the model array
model_s0_c1_uc[:,0] = 2.5
model_s0_c2_uc[:,0] = 2.5
model_s0_c3_uc[:,0] = 2.5
model_s0_c4_uc[:,0] = 2.5


# Store models

np.save('models/model_s0_c1_uc', model_s0_c1_uc)
np.save('models/model_s0_c2_uc', model_s0_c2_uc)
np.save('models/model_s0_c3_uc', model_s0_c3_uc)
np.save('models/model_s0_c4_uc', model_s0_c4_uc)

np.save('models/model_s1_c1_uc', model_s1_c1_uc)
np.save('models/model_s1_c2_uc', model_s1_c2_uc)
np.save('models/model_s1_c3_uc', model_s1_c3_uc)
np.save('models/model_s1_c4_uc', model_s1_c4_uc)

np.save('models/model_s2_c1_uc', model_s2_c1_uc)
np.save('models/model_s2_c2_uc', model_s2_c2_uc)
np.save('models/model_s2_c3_uc', model_s2_c3_uc)
np.save('models/model_s2_c4_uc', model_s2_c4_uc)

np.save('models/model_s3_c1_uc', model_s5_c1_uc)
np.save('models/model_s3_c2_uc', model_s5_c2_uc)
np.save('models/model_s3_c3_uc', model_s5_c3_uc)
np.save('models/model_s3_c4_uc', model_s5_c4_uc)

np.save('models/model_s4_c1_uc', model_s10_c1_uc)
np.save('models/model_s4_c2_uc', model_s10_c2_uc)
np.save('models/model_s4_c3_uc', model_s10_c3_uc)
np.save('models/model_s4_c4_uc', model_s10_c4_uc)

np.save('models/model_s1_c1_ur', model_s1_c1_ur)
np.save('models/model_s1_c2_ur', model_s1_c2_ur)
np.save('models/model_s1_c3_ur', model_s1_c3_ur)
np.save('models/model_s1_c4_ur', model_s1_c4_ur)

np.save('models/model_s2_c1_ur', model_s2_c1_ur)
np.save('models/model_s2_c2_ur', model_s2_c2_ur)
np.save('models/model_s2_c3_ur', model_s2_c3_ur)
np.save('models/model_s2_c4_ur', model_s2_c4_ur)

np.save('models/model_s3_c1_ur', model_s5_c1_ur)
np.save('models/model_s3_c2_ur', model_s5_c2_ur)
np.save('models/model_s3_c3_ur', model_s5_c3_ur)
np.save('models/model_s3_c4_ur', model_s5_c4_ur)

np.save('models/model_s4_c1_ur', model_s10_c1_ur)
np.save('models/model_s4_c2_ur', model_s10_c2_ur)
np.save('models/model_s4_c3_ur', model_s10_c3_ur)
np.save('models/model_s4_c4_ur', model_s10_c4_ur)
