#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import segyio
import pandas as pd
import matplotlib.pyplot as pl
import numpy as np

from importsegy import readSEGYbasicattributes
from importsegy import readSEGY
from importsegy import print_headers


seismic_all       = []
bin_headers_all   = []
text_headers_all  = []
trace_headers_all = []

#QC trace headers
key1 = 'CDP_X'
key2 = 'CDP_Y'
pl.figure(figsize=(18,6))

folder="../segy/set2_Lines2D_inlines/"
for i in range(12,25):
    filename=folder+"line"+str(i)+".sgy"
    print(filename)
    
    # get basic attributes
    n_traces, n_samples, sample_rate, twt = readSEGYbasicattributes(filename)

    # import all segy information
    seismic, bin_headers, text_headers, trace_headers = readSEGY(filename) 

    # print useful information    
    print_headers(seismic,bin_headers,text_headers,trace_headers, \
                  n_traces, n_samples, sample_rate, twt)    
    
    # create a list
    seismic_all.append(seismic)
    bin_headers_all.append(bin_headers)
    text_headers_all.append(text_headers)
    trace_headers_all.append(trace_headers)

    # plot geometry
    pl.plot(trace_headers[key1],trace_headers[key2],'r*')


pl.title('Quality control:  ' + key1 + ' vs ' + key2)
pl.grid()
pl.show()

#Plot seismic
vm = np.percentile(seismic_all[0][:,:], 95)
pl.figure(figsize=(18,6))
pl.imshow(seismic_all[0].T, cmap="gray", vmin=-vm, vmax=vm, aspect='auto')
pl.colorbar()
pl.show()