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


# Get all header keys
header_keys = segyio.tracefield.keys

filename="../segy/set2_Lines2D_inlines/line12.sgy"
with segyio.open(filename,ignore_geometry=True) as f:
    print(f.tracecount)
    seismicA       = f.trace.raw[:]
    textheader     = f.text[0]
    bin_headers    = f.bin
    trace_headerA = parse_trace_headers(f, f.tracecount)

filename="../segy/set2_Lines2D_inlines/line13.sgy"
with segyio.open(filename,ignore_geometry=True) as f:
    print(f.tracecount)
    seismicB = f.trace.raw[:]
    trace_headerB = parse_trace_headers(f, f.tracecount)

seismic_merge = np.concatenate((seismicA,seismicB),axis=0)

n_samples    = seismic_merge.shape[1]
n_traces    = seismic_merge.shape[0]
sample_rate = 4 # ms

path = '../segy/Newsegy.sgy'
# Create a segy from a 2D matrix
segyio.tools.from_array2D(path,seismic_merge)

with segyio.open(path,'r+',ignore_geometry=True) as f:
    # Copy bin header
    f.bin = bin_headers
    
    # Update bin header
    f.bin.update({segyio.BinField.Interval : sample_rate*1000})                
    f.bin.update({segyio.BinField.Samples  : n_samples})
    f.bin.update({segyio.BinField.Traces   : n_traces})

    # Copy text header
    f.text[0] = textheader

    # Copy trace header
    
    # for k,v in header_keys.item():
    #     print(k,v)
    #     # print(f.attributes(v)[:])
        # print(trace_headersA.attributes(v)[:])

    

     
    # set fixed value in all trace headers
    for x in f.header[:]:
        x.update({segyio.TraceField.TRACE_SAMPLE_COUNT    : n_samples })
        x.update({segyio.TraceField.TRACE_SAMPLE_INTERVAL : sample_rate*1000 })