import segyio
import pandas as pd
import matplotlib.pyplot as pl
import numpy as np
import scipy.signal

from importsegy import readSEGYbasicattributes
from importsegy import readSEGY
from importsegy import print_headers
from importsegy import plot_segy
from importsegy import parse_trace_headers

filename="../segy/set2_Lines2D_inlines/line12.sgy"
with segyio.open(filename,ignore_geometry=True) as f:
    print('f.tracecount=',f.tracecount)
    seismicA    = f.trace.raw[:]
    textheader  = f.text[0]
    bin_headers = f.bin   
    # get trace headers values
    ilA         = f.attributes(segyio.TraceField.INLINE_3D)[:]
    xlA         = f.attributes(segyio.TraceField.CROSSLINE_3D)[:]
    cdpxA       = f.attributes(segyio.TraceField.CDP_X)[:]
    cdpyA       = f.attributes(segyio.TraceField.CDP_Y)[:]

filename="../segy/set2_Lines2D_inlines/line13.sgy"
with segyio.open(filename,ignore_geometry=True) as f:
    print('f.tracecount=',f.tracecount)
    seismicB    = f.trace.raw[:]
    # get trace headers values
    ilB         = f.attributes(segyio.TraceField.INLINE_3D)[:]
    xlB         = f.attributes(segyio.TraceField.CROSSLINE_3D)[:]
    cdpxB       = f.attributes(segyio.TraceField.CDP_X)[:]
    cdpyB       = f.attributes(segyio.TraceField.CDP_Y)[:]

seismic_merge   = np.concatenate((seismicA,seismicB),axis=0)
il_merge        = np.concatenate((ilA     ,ilB)     ,axis=0)
xl_merge        = np.concatenate((xlA     ,xlB)     ,axis=0)
cdpx_merge      = np.concatenate((cdpxA   ,cdpxB)   ,axis=0)
cdpy_merge      = np.concatenate((cdpyA   ,cdpyB)   ,axis=0)

n_samples       = seismic_merge.shape[1]
n_traces        = seismic_merge.shape[0]
sample_rate     = 4 # ms

path            = '../segy/Newsegy.sgy'

# Create a segy from a 2D matrix
segyio.tools.from_array2D(path,seismic_merge)

# read empty segy
SEGY            = segyio.open(path,'r+',ignore_geometry=True)
# set trace headers values
for idx, key in enumerate(SEGY.header):
    key.update({segyio.TraceField.INLINE_3D    : il_merge[idx]})
    key.update({segyio.TraceField.CROSSLINE_3D : xl_merge[idx]})
    key.update({segyio.TraceField.CDP_X        : cdpx_merge[idx]})
    key.update({segyio.TraceField.CDP_Y        : cdpy_merge[idx]})

# SEGY.close()