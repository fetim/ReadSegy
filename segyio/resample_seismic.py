import segyio
import pandas as pd
import matplotlib.pyplot as pl
import numpy as np
import scipy.signal

from importsegy import readSEGYbasicattributes
from importsegy import readSEGY
from importsegy import print_headers

filename="../segy/set2_Lines2D_inlines/line12.sgy"

# get basic attributes
n_traces, n_samples, sample_rate, twt = readSEGYbasicattributes(filename)

# import all segy information
seismic, bin_headers, text_headers, trace_headers = readSEGY(filename) 

# # print useful information    
# print_headers(seismic,bin_headers,text_headers,trace_headers, \
#                 n_traces, n_samples, sample_rate, twt)

output ="../segy/set2_Lines2D_inlines/line12_resample.sgy"

new_sampling = 8  # Should be a multiple of the original sampling rate
sampling_ratio = int(new_sampling/sample_rate)

with segyio.open(filename,ignore_geometry=True) as segyfile:
    # Copy metadata from original segy
    struc_proprities =  segyio.tools.metadata(segyfile)
    # Edit: set right number of samples
    struc_proprities.samples = struc_proprities.samples[0:int(segyfile.samples.size):sampling_ratio]
    # Create new segy
    with segyio.create(output,struc_proprities) as segyfileout:        
        # Copy text header 
        segyfileout.text[0] = segyfile.text[0]
        # Copy binary header
        segyfileout.bin     = segyfile.bin
        # # Copy trace header
        segyfileout.header = segyfile.header        
        # Resampling traces
        for ix,trace in enumerate(segyfile.trace):
            segyfileout.trace[ix] = scipy.signal.resample(trace,int(len(trace)/sampling_ratio))            
        
        # set fixed value in all headers
        for x in segyfileout.header[:]:
            x.update({segyio.TraceField.TRACE_SAMPLE_COUNT    : segyfileout.samples.size })
            x.update({segyio.TraceField.TRACE_SAMPLE_INTERVAL : new_sampling*1000 })


        # insert correct sample rate
        segyfileout.bin.update(hdt=new_sampling*1000)
        
        # insert correct trace length
        segyfileout.bin.update(hns=len(struc_proprities.samples)) 