import segyio
import pandas as pd
import matplotlib.pyplot as pl
import numpy as np
import scipy.signal

from importsegy import readSEGYbasicattributes
from importsegy import readSEGY
from importsegy import print_headers
from importsegy import plot_segy


filename="../segy/set2_Lines2D_inlines/line12.sgy"

with segyio.open(filename,ignore_geometry=True) as f:
    seismic12 = f.trace.raw[:]
    textheader = f.text[0]

filename="../segy/set2_Lines2D_inlines/line13.sgy"

with segyio.open(filename,ignore_geometry=True) as f:
    seismic13 = f.trace.raw[:]

seismic_merge = np.concatenate((seismic12,seismic13),axis=0)

n_samples    = seismic_merge.shape[1]
n_traces    = seismic_merge.shape[0]
sample_rate = 4 # ms

path = '../segy/Newsegy.sgy'
# Create a segy from a 2D matrix
segyio.tools.from_array2D(path,seismic_merge)

with segyio.open(path,'r+',ignore_geometry=True) as f:
    f.text[0] = textheader
    f.bin.update({segyio.BinField.Interval : sample_rate*1000})                
    f.bin.update({segyio.BinField.Samples  : n_samples})
    f.bin.update({segyio.BinField.Traces   : n_traces})

# set fixed value in all headers
    for x in f.header[:]:
        x.update({segyio.TraceField.TRACE_SAMPLE_COUNT    : n_samples })
        x.update({segyio.TraceField.TRACE_SAMPLE_INTERVAL : sample_rate*1000 })