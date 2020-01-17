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

        # Readind data
        seismic     = segyfile.trace.raw[:]  # Get all data into memory (could cause on big files)
        n_traces    = segyfile.tracecount

        # Load headers
        bin_headers   = segyfile.bin    
        text_headers  = parse_text_header(segyfile)
        trace_headers = parse_trace_headers(segyfile, n_traces)

    #return seismic, bin_headers, trace_headers
    return seismic, bin_headers, text_headers, trace_headers

def readSEGYbasicattributes(path):
    with segyio.open(path, "r",ignore_geometry=True) as segyfile:
        # Get basic attributes
        n_traces = segyfile.tracecount
        n_samples = segyfile.samples.size
        sample_rate = segyio.tools.dt(segyfile)/1000
        samples = segyfile.samples

    return n_traces, n_samples, sample_rate, samples


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
                  n_traces, n_samples, sample_rate, samples):
        
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
    print('%40s %8d'    % ('n_traces    = ',n_traces )   )
    print('%40s %8d'    % ('n_samples   = ',n_samples )  )
    print('%40s %8d ms' % ('sample_rate = ',sample_rate ))
    print('%40s %8d ms' % ('samples[ 0] = ',samples[0] )     )
    print('%40s %8d ms' % ('samples[-1] = ',samples[-1])     )

def plot_segy(file):
    # Load data
    with segyio.open(file, ignore_geometry=True) as f:
        # Get basic attributes
        n_traces = f.tracecount
        sample_rate = segyio.tools.dt(f) / 1000
        n_samples = f.samples.size
        twt = f.samples
        data = f.trace.raw[:]
    # Plot    
    vm = np.percentile(data, 95)
    pl.figure(figsize=(18, 8))    
    extent = [1, n_traces, twt[-1], twt[0]]  # define extent
    pl.imshow(data.T, cmap="RdBu", vmin=-vm, vmax=vm, aspect='auto', extent=extent)
    pl.xlabel('CDP number')
    pl.ylabel('TWT [ms]')
    pl.title(f'{file}')    

if __name__ =="__main__":

    
     
    filename="../segy/Newsegy.sgy"
    
    plot_segy(filename)

    # filename="../segy/set2_Lines2D_inlines/line12_resample.sgy"
    # plot_segy(filename)

    # get basic attributes
    n_traces, n_samples, sample_rate, twt = readSEGYbasicattributes(filename)

    # import all segy information
    seismic, bin_headers, text_headers, trace_headers = readSEGY(filename) 

    # print useful information    
    print_headers(seismic,bin_headers,text_headers,trace_headers, \
                  n_traces, n_samples, sample_rate, twt)

    pl.show()
