#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import segyio
import pandas as pd
import matplotlib.pyplot as pl
import numpy as np

from importsegy import readSEGYbasicattributes
from importsegy import readSEGY
from importsegy import print_headers


seismic_all_xline       = []
bin_headers_all_xline   = []
text_headers_all_xline  = []
trace_headers_all_xline = []

n_traces_all_xline      = [] 
n_samples_all_xline     = [] 
sample_rate_all_xline   = []
twt_all_xline           = []

#QC trace headers
key1 = 'CDP_X'
key2 = 'CDP_Y'
pl.figure(figsize=(18,6))

folder="../segy/set1_Lines2D_xlines/"
for i in range(1,12,4):
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
    seismic_all_xline.append(seismic)
    bin_headers_all_xline.append(bin_headers)
    text_headers_all_xline.append(text_headers)
    trace_headers_all_xline.append(trace_headers)

    n_traces_all_xline.append(n_traces)
    n_samples_all_xline.append(n_samples)
    sample_rate_all_xline.append(sample_rate)
    twt_all_xline.append(twt)

    # plot geometry
    pl.plot(trace_headers[key1],trace_headers[key2],'b*')

seismic_all_inline       = []
bin_headers_all_inline   = []
text_headers_all_inline  = []
trace_headers_all_inline = []

n_traces_all_inline      = [] 
n_samples_all_inline     = [] 
sample_rate_all_inline   = []
twt_all_inline           = []

folder="../segy/set2_Lines2D_inlines/"
for i in range(12,25,4):
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
    seismic_all_inline.append(seismic)
    bin_headers_all_inline.append(bin_headers)
    text_headers_all_inline.append(text_headers)
    trace_headers_all_inline.append(trace_headers)

    n_traces_all_inline.append(n_traces)
    n_samples_all_inline.append(n_samples)
    sample_rate_all_inline.append(sample_rate)
    twt_all_inline.append(twt)

    # plot geometry
    pl.plot(trace_headers[key1],trace_headers[key2],'r*')


pl.title('Quality control:  ' + key1 + ' vs ' + key2)
pl.grid()
pl.show()

#Plot seismic
vm = np.percentile(seismic_all_xline[0][:,:], 95)
pl.figure(figsize=(18,6))
pl.imshow(seismic_all_inline[0].T, cmap="gray", vmin=-vm, vmax=vm, aspect='auto')
pl.colorbar()
pl.show()


# plot geometry
#QC trace headers
key1 = 'CDP_X'
key2 = 'CDP_Y'
pl.figure(figsize=(18,6))
for i in range(0,len(trace_headers_all_inline)):
    pl.plot(trace_headers_all_inline[i][key1],trace_headers_all_inline[i][key2],'r*')
            
for i in range(0,len(trace_headers_all_xline)):
    pl.plot(trace_headers_all_xline[i][key1],trace_headers_all_xline[i][key2],'r*')

pl.grid()
pl.show()
