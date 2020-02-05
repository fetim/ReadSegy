#!/opt/anaconda3/bin/python
import segyio
import matplotlib.pyplot as pl
import numpy as np


folder   = "/home/felipe/Desktop/Dados_Buzios/"
filename = "R0276_BS_500_FRANCO_FLORIM_PSDM_VEL.3D.PSDM"

SEGY     = segyio.open(folder+filename+".sgy",ignore_geometry=True)

# explore traceheader
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
N_XL = int(np.abs((SEGY.attributes(225)[len(SEGY.tracecount-1] - SEGY.attributes(225)[0]))/inc_XL) + 1
N_xline = 863

select_XL_index = int(np.abs((select_XL - SEGY.attributes(225)[0]))/inc_XL)

#
# N_traces = 1037326

# #Xline 3824 - 863*582 - 863*583

# # inline
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

