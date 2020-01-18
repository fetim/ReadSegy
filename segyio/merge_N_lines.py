import segyio
import matplotlib.pyplot as pl
import numpy as np

bin_headers   = []
text_headers  = []
il            = []
xl            = []
cdpx          = []
cdpy          = []
seismic       = []

folder1="../segy/set1_Lines2D_xlines/"
folder2="../segy/set2_Lines2D_inlines/"
for idx, i in enumerate(range(1,13)):
    if i < 12:
        filename=folder1+"line"+str(i)+".sgy"
        print(filename, 'Importing segy ', idx)
    else:
        filename=folder2+"line"+str(i)+".sgy"
        print(filename, 'Importing segy ', idx)
        
    with segyio.open(filename,ignore_geometry=True) as SEGY:
        print('tracecount=',SEGY.tracecount)
        seismic.append(SEGY.trace.raw[:])

        # get trace headers values
        il.append(SEGY.attributes(segyio.TraceField.INLINE_3D)[:])
        xl.append(SEGY.attributes(segyio.TraceField.CROSSLINE_3D)[:])
        cdpx.append(SEGY.attributes(segyio.TraceField.CDP_X)[:])
        cdpy.append(SEGY.attributes(segyio.TraceField.CDP_Y)[:])
        
        if (idx < 1):
            n_samples    = SEGY.samples.size
            bin_headers  = SEGY.bin
            text_headers = SEGY.text[0]

n_traces = 0 
for section in seismic:
    n_traces += len(section)

seismic_merge = np.zeros([n_traces,n_samples])
il_merge      = np.squeeze(np.zeros([n_traces,1])).astype('int32')
xl_merge      = np.squeeze(np.zeros([n_traces,1])).astype('int32')
cdpx_merge    = np.squeeze(np.zeros([n_traces,1])).astype('int32')
cdpy_merge    = np.squeeze(np.zeros([n_traces,1])).astype('int32')

for lines in range(24):    
    seismic_merge    = np.concatenate((seismic_merge,seismic[idx]),axis=0)
    il_merge         = np.concatenate((il_merge,il[idx]),axis=0)
    xl_merge         = np.concatenate((xl_merge,xl[idx]),axis=0)
    cdpx_merge       = np.concatenate((cdpx_merge,cdpx[idx]),axis=0)
    cdpy_merge       = np.concatenate((cdpy_merge,cdpy[idx]),axis=0)

path            = '../segy/Newsegy.sgy'
# Create a segy from a 2D matrix
segyio.tools.from_array2D(path,seismic_merge)

# read empty segy
SEGY            = segyio.open(path,'r+',ignore_geometry=True)
# Copy binary header
SEGY.bin     = bin_headers
# Copy text header 
SEGY.text[0] = text_headers

# set trace headers values
for idx, key in enumerate(SEGY.header):
    key.update({segyio.TraceField.INLINE_3D    : il_merge[idx]})
    key.update({segyio.TraceField.CROSSLINE_3D : xl_merge[idx]})
    key.update({segyio.TraceField.CDP_X        : cdpx_merge[idx]})
    key.update({segyio.TraceField.CDP_Y        : cdpy_merge[idx]})

SEGY.close()


