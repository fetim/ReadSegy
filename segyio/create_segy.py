import segyio
import matplotlib.pyplot as pl
import numpy as np

from segyio_tools import readSEGYbasicattributes
from segyio_tools import readSEGY
from segyio_tools import print_headers
from segyio_tools import plot_segy

path = '../segy/Newsegy.sgy'

n_traces = 100
n_samples = 1001
sample_rate = 2 # ms
array2d = np.zeros([n_traces,n_samples]) + 1500

for i in range(0,n_traces):
    for j in range(0,n_samples):
        if (j> int(n_samples/2)):
            array2d[i,j] = 2000

# Create a segy from a 2D matrix
segyio.tools.from_array2D(path,array2d)

with segyio.open(path,'r+',ignore_geometry=True) as f:
    # Update bin header
    f.bin.update({segyio.BinField.Interval : sample_rate*1000})                
    f.bin.update({segyio.BinField.Samples  : n_samples})
    f.bin.update({segyio.BinField.Traces   : n_traces})

    # set fixed value in all trace headers
    for x in f.header[:]:
        x.update({segyio.TraceField.TRACE_SAMPLE_COUNT    : f.samples.size })
        x.update({segyio.TraceField.TRACE_SAMPLE_INTERVAL : sample_rate*1000 })
