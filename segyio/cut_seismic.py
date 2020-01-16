import segyio
import pandas as pd
import matplotlib.pyplot as pl
import numpy as np

from importsegy import readSEGYbasicattributes
from importsegy import readSEGY
from importsegy import print_headers

filename="../segy/set2_Lines2D_inlines/line12.sgy"

# get basic attributes
n_traces, n_samples, sample_rate, twt = readSEGYbasicattributes(filename)

# import all segy information
seismic, bin_headers, text_headers, trace_headers = readSEGY(filename) 

# print useful information    
print_headers(seismic,bin_headers,text_headers,trace_headers, \
                n_traces, n_samples, sample_rate, twt)

output="../segy/set2_Lines2D_inlines/line12_edited.sgy"

# Define the sample index to cut on
cut_time = 2000
cut_sample = int(cut_time / sample_rate)+1

with segyio.open(filename,ignore_geometry=True) as segyfile:
    # Copy metadata from original segy
    struc_proprities =  segyio.tools.metadata(segyfile)
    # Edit: removing samples > 2000 ms
    struc_proprities.samples = struc_proprities.samples[:cut_sample]
    # Create new segy
    with segyio.create(output,struc_proprities) as segyfileout:
        # Copy text header 
        segyfileout.text[0] = segyfile.text[0]
        # Copy binary header
        segyfileout.bin     = segyfile.bin
        # insert correct trace length
        segyfileout.bin.update(hns=len(struc_proprities.samples)) 
        # Copy trace header
        segyfileout.header = segyfile.header
        # Copy data
        segyfileout.trace = segyfile.trace
        