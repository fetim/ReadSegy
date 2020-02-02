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
    print('%40s: %8s - %8s \n' % ('Trace','first','last'))

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

def updateSEGYbinaryheader(SEGY):
    # Binary Header according ANP
    # * Highly recommended information, recommended by SEG-Y standard
    # @ Mandatory
    SEGY.bin[segyio.BinField.JobID]                 = 0   #3201-3204  Job identification number
    SEGY.bin[segyio.BinField.LineNumber]            = 320 #3205-3208* For 3-D poststack data, this will typically contain the in-line number 
    SEGY.bin[segyio.BinField.ReelNumber]            = 0   #3209-3212* Reel number
    # SEGY.bin[segyio.BinField.Traces]              = 0   #3213-3214* Number of data traces per ensemble. Mandatory for prestack data.
    SEGY.bin[segyio.BinField.AuxTraces]             = 0   #3215-3216* Number of auxiliary traces per ensemble. Mandatory for prestack data.
    # SEGY.bin[segyio.BinField.Interval]            = 0   #3217-3218* Sample interval in microseconds (µs). Mandatory for all data types.
    # SEGY.bin[segyio.BinField.IntervalOriginal]    = 0   #3219-3220  Sample interval in microseconds (µs) of original field recording.
    # SEGY.bin[segyio.BinField.Samples]             = 0   #3221-3222* Number of samples per data trace. Mandatory for all types of data. 
    SEGY.bin[segyio.BinField.SamplesOriginal]       = 0   #3223-3224  Number of samples per data trace for original field recording.
    SEGY.bin[segyio.BinField.Format]                = 1   #3225-3226@ Data sample format code. Mandatory for all data. For ANP - BDEP it has to be = 1
    SEGY.bin[segyio.BinField.EnsembleFold]          = 0   #3227-3228* Ensemble fold — The expected number of data traces per trace ensemble (e.g. the CMP fold). Highly recommended for all types of data.
    SEGY.bin[segyio.BinField.SortingCode]           = 2   #3229-3230@ Trace sorting code (i.e. type of ensemble) : 
    #                                                                 -1 = Other (should be explained in user Extended Textual File Header stanza 
    #                                                                 0 = Unknown 
    #                                                                 1 = As recorded (no sorting) 
    #                                                                 2 = CDP ensemble 
    #                                                                 3 = Single fold continuous profile  
    #                                                                 4 = Horizontally stacked 
    #                                                                 5 = Common source point 
    #                                                                 6 = Common receiver point 
    #                                                                 7 = Common offset point 
    #                                                                 8 = Common mid-point 
    #                                                                 9 = Common conversion point
    SEGY.bin[segyio.BinField.VerticalSum]           = 0   #3231-3232 Vertical sum code: 1 = no sum, 2 = two sum, …, N = M-1 sum (M = 2 to 32,767)
    SEGY.bin[segyio.BinField.SweepFrequencyStart]   = 0   #3233-3234 Sweep frequency at start (Hz).
    SEGY.bin[segyio.BinField.SweepFrequencyEnd]     = 0   #3235-3236 Sweep frequency at end (Hz).
    SEGY.bin[segyio.BinField.SweepLength]           = 0   #3237-3238 Sweep length (ms)
    SEGY.bin[segyio.BinField.Sweep]                 = 0   #3239-3240 Sweep type code: 1 = linear 2 = parabolic 3 = exponential 4 = other
    SEGY.bin[segyio.BinField.SweepChannel]          = 0   #3241-3242 Trace number of sweep channel.
    SEGY.bin[segyio.BinField.SweepTaperStart]       = 0   #3243-3244 Sweep trace taper length in milliseconds at start if tapered (the taper starts at zero time and is effective for this length).
    SEGY.bin[segyio.BinField.SweepTaperEnd]         = 0   #3245-3246 Sweep trace taper length in milliseconds at end (the ending taper starts at sweep length minus the taper length at end).
    SEGY.bin[segyio.BinField.Taper]                 = 0   #3247-3248 Taper type: 1 = linear 2 = cos2 3 = other
    SEGY.bin[segyio.BinField.CorrelatedTraces]      = 0   #3249-3250 Correlated data traces: 1 = no 2 = yes
    SEGY.bin[segyio.BinField.BinaryGainRecovery]    = 0   #3251-3252 Binary gain recovered:1 = yes 2 = no
    SEGY.bin[segyio.BinField.AmplitudeRecovery]     = 0   #3253-3254 Amplitude recovery method: 1 = none 2 = spherical divergence 3 = AGC 4 = other
    SEGY.bin[segyio.BinField.MeasurementSystem]     = 1   #3255-3256@ Measurement system: Highly recommended for all types of data. 1 = Meters 2 = Feet
    SEGY.bin[segyio.BinField.ImpulseSignalPolarity] = 1   #3257-3258@ Impulse signal polarity 
    #                                                                 1 = Increase in pressure or upward geophone case movement gives negative number on tape.
    #                                                                 2 = Increase in pressure or upward geophone case movement gives positive number on tape.
    SEGY.bin[segyio.BinField.VibratoryPolarity]     = 0   #3259-3260  Vibratory polarity code: Seismic signal lags pilot signal by
    #                                                                 1 = 337.5° to 22.5° 2 = 22.5° to 67.5° 3 = 67.5° to 112.5° 4 = 112.5° to 157.5°
    #                                                                 5 = 157.5° to 202.5° 6 = 202.5° to 247.5° 7 = 247.5° to 292.5° 8 = 292.5° to 337.5°

    # 3261-3500 Unassigned

    SEGY.bin[segyio.BinField.SEGYRevision]         = 0    #3501-3502 SEG Y Format Revision Number.
    #                                                                This is a 16-bit unsigned value with a Q- point between the first and second bytes. 
    #                                                                Thus for SEG Y Revision 1.0, as defined in this document, this will be recorded as 0100.
    #                                                                This field is mandatory for all versions of SEG Y, although a value of zero indicates 
    #                                                                “traditional” SEG Y conforming to the 1975 standard.

    SEGY.bin[segyio.BinField.TraceFlag]            = 0    #3503-3504 Fixed length trace flag. 
    #                                                                A value of one indicates that all traces in this SEG Y file are guaranteed to have the 
    #                                                                same sample interval and number of samples, as specified in Textual File Header bytes 
    #                                                                3217-3218 and 3221-3222. A value of zero indicates that the length of the traces in the
    #                                                                file may vary and the number of samples in bytes 115-116 of the Trace Header must be examined to 
    #                                                                determine the actual length of each trace. This field is mandatory for all versions of SEG Y, 
    #                                                                although a value of zero indicates “traditional” SEG Y conforming to the 1975 standard.

    SEGY.bin[segyio.BinField.ExtendedHeaders]     = 0     #3505-3506  Number of 3200-byte, Extended Textual File Header records following theBinary Header.
    #                                                                 A value of zero indicates there are no Extended Textual File Header records (i.e. this
    #                                                                 file has no Extended Textual File Header(s)). A value of -1 indicates that there are a variable
    #                                                                 number of Extended Textual File Header records and the end of the Extended Textual File Header
    #                                                                 is denoted by an ((SEG: EndText)) stanza in the final record. A positive value indicates that 
    #                                                                 there are exactly that many Extended Textual File Header records. Note that, although the exact 
    #                                                                 number of Extended Textual File Header records may be a useful piece of information, it will not
    #                                                                 always be known at the time the Binary Header is written and it is not mandatory that a positive 
    #                                                                 value be recorded here. This field is mandatory for all versions of SEG Y, although a value of
    #                                                                 zero indicates “traditional” SEG Y conforming to the 1975 standard.

    # 3507-3600 Unassigned

    return SEGY

if __name__ =="__main__":
         
    filename="../segy/set2_Lines2D_inlines/line12.sgy"
    
    plot_segy(filename)

    # filename="../segy/set1_Lines2D_xlines/line1.sgy"
    # plot_segy(filename)

    # get basic attributes
    n_traces, n_samples, sample_rate, twt = readSEGYbasicattributes(filename)

    # import all segy information
    seismic, bin_headers, text_headers, trace_headers = readSEGY(filename) 

    # print useful information    
    print_headers(seismic,bin_headers,text_headers,trace_headers, \
                  n_traces, n_samples, sample_rate, twt)

    pl.show()
