#!/opt/anaconda3/bin/python
import segyio
import matplotlib.pyplot as pl
import numpy as np
from segyio_tools import savebinaryfile
folder   = "../segy/"
filename = "0212-0019_Amplitudes"

SEGY     = segyio.open(folder+filename+".sgy",ignore_geometry=True)

# get he
headers = segyio.tracefield.keys

for k,v in headers.items():    
    print(k,v,SEGY.attributes(v)[0],SEGY.attributes(v)[SEGY.tracecount-1])

# pl.plot(SEGY.attributes(223)[int(863*500):int(863*600)])
# pl.show()

select_IL = 4328
inc_IL = 2
N_IL = int(np.abs((SEGY.attributes(223)[SEGY.tracecount-1] - SEGY.attributes(223)[0]))/inc_IL) + 1
N_inline = 1202

select_IL_index = int(np.abs((select_IL - SEGY.attributes(223)[0]))/inc_IL)

select_XL = 3824
inc_XL = 4
N_XL = int(np.abs((SEGY.attributes(225)[SEGY.tracecount-1] - SEGY.attributes(225)[0]))/inc_XL) + 1
N_xline = 863

select_XL_index = int(np.abs((select_XL - SEGY.attributes(225)[0]))/inc_XL)

# inline
velocitymodel_IL = np.zeros([SEGY.samples.size,N_XL])

velocitymodel_IL = SEGY.trace.raw[ N_XL*select_IL_index : N_XL*(select_IL_index+1)].T
pl.imshow(velocitymodel_IL)
pl.show()

# Crossline
velocitymodel_XL = np.zeros([SEGY.samples.size,N_IL])

for i in range(0,N_IL):    
    velocitymodel_XL[:,i]  = SEGY.trace.raw[i*N_XL+select_XL_index].T

pl.imshow(velocitymodel_XL)
pl.show()

filename = "inline_"+str(select_IL)+"_buzios_1001z_1402x_dz10m_dx25m"
savebinaryfile(velocitymodel_XL.shape[0],velocitymodel_IL.shape[1],velocitymodel_IL,folder+filename+".bin")

filename = "xline_"+str(select_XL)+"_buzios_1001z_863x_dz10m_dx50m"
savebinaryfile(velocitymodel_XL.shape[0],velocitymodel_XL.shape[1],velocitymodel_XL,folder+filename+".bin")

