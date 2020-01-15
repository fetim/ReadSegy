#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:59:43 2019

@author: felipe
"""
#%%
import segyio
import pandas as pd
import matplotlib.pyplot as pl
import numpy as np

import re
from scipy import ndimage as ndi
from shutil import copyfile
from skimage import exposure

def readSEGY(path):
    with segyio.open(path, "r",ignore_geometry=True) as segyfile:
        # Memory map file for faster reading (especially if file is big...)
        segyfile.mmap()
        print("Reading ", path)

        # Get basic attributes
        n_traces    = segyfile.tracecount
        sample_rate = segyio.tools.dt(segyfile) / 1000
        n_samples   = segyfile.samples.size
        twt         = segyfile.samples

        # Readind data
        seismic     = segyfile.trace.raw[:]  # Get all data into memory (could cause on big files)

        # Load headers
        bin_headers   = segyfile.bin    
        text_headers  = parse_text_header(segyfile)
        trace_headers = parse_trace_headers(segyfile, n_traces)

    #return seismic, bin_headers, trace_headers
    return seismic, bin_headers, text_headers, trace_headers

def readSEGYbasicattributes(path):
    with segyio.open(path, "r",ignore_geometry=True) as segyfile:
        n_traces = segyfile.tracecount
        n_samples = segyfile.samples.size
        sample_rate = segyio.tools.dt(segyfile)/1000
        twt = segyfile.samples

    return n_traces, n_samples, sample_rate, twt


def parse_trace_headers(segyfile, n_traces):
    '''
    Parse the segy file trace headers into a pandas dataframe.
    Column names are defined from segyio internal tracefield
    One row per trace
    '''
    # Get all header keys
    headers = segyio.tracefield.keys
    # Initialize dataframe with trace id as index and headers as columns
    df = pd.DataFrame(index=range(1, n_traces + 1),
                      columns=headers.keys())
    # Fill dataframe with all header values
    for k, v in headers.items():
        df[k] = segyfile.attributes(v)[:]
    return df

def parse_text_header(segyfile):
    '''
    Format segy text header into a readable, clean dict
    '''
    raw_header = segyio.tools.wrap(segyfile.text[0])
    # Cut on C*int pattern
    cut_header = re.split(r'C ', raw_header)[1::]
    # Remove end of line return
    text_header = [x.replace('\n', ' ') for x in cut_header]
    text_header[-1] = text_header[-1][:-2]
    # Format in dict
    clean_header = {}
    i = 1
    for item in text_header:
        key = "C" + str(i).rjust(2, '0')
        i += 1
        clean_header[key] = item
    return clean_header

def print_headers(seismic,bin_headers,text_headers,trace_headers, \
                  n_traces, n_samples, sample_rate, twt):
        
    print(' \n \n \n Binary Header')
    for line in bin_headers:
        print('%40s: %8d ' % (line, bin_headers[line]))    

    print(' \n \n \n Text Header \n')
    for line in text_headers:
        print(line, text_headers[line])

    print(' \n \n \n Trace Header keys')
    for key in trace_headers.columns:
        print('%40s: %8d - %8d' % (key, trace_headers[key][1] ,trace_headers[key][n_traces] ))
    
    print(' \n \n \n Basic attributes')
    print('%40s %8d'    % ('Number of traces  = ',n_traces ))
    print('%40s %8d'    % ('Number of samples = ',n_samples ))
    print('%40s %8d ms' % ('Sample rate = '      ,sample_rate ))
    print('%40s %8d ms' % ('start time = '       ,twt[0] ))
    print('%40s %8d ms' % ('end time = '         ,twt[-1]))

if __name__ =="__main__":

    filename="../segy/set2_Lines2D_inlines/line12.sgy"

    # get basic attributes
    n_traces, n_samples, sample_rate, twt = readSEGYbasicattributes(filename)

    # import all segy information
    seismic, bin_headers, text_headers, trace_headers = readSEGY(filename) 

    # print useful information    
    print_headers(seismic,bin_headers,text_headers,trace_headers, \
                  n_traces, n_samples, sample_rate, twt)

    #QC trace headers
    key1 = 'CDP_X'
    key2 = 'CDP_Y'

    pl.figure(figsize=(18,6))
    pl.plot(trace_headers[key1],trace_headers[key2],'r*')

    pl.title('Quality control:  ' + key1 + ' vs ' + key2)
    pl.grid()
    pl.show()

    #Plot seismic
    vm = np.percentile(seismic[:,:], 95)
    pl.figure(figsize=(18,6))
    pl.imshow(seismic.T, cmap="gray", vmin=-vm, vmax=vm, aspect='auto')
    pl.colorbar()
    pl.show()