import segyio
import matplotlib.pyplot as pl
import numpy as np

def readbinaryfile(dim1,dim2,filename):
      """
      readbinaryfile - Functions that read a binary file.
      Usage
      Input:
      dim1     = Number of sample of 1st Dimension
      dim2     = Number of sample of 2nd Dimension
      filename = path of binary file     
      """
      print("\n loading ", filename) 
      with open(filename, 'rb') as f:    
            data   = np.fromfile(filename, dtype= np.float32, count= dim1*dim2)
            matrix = np.reshape(data, [dim1,dim2], order='F')
      return matrix


#parameters
Nx = 72
Nt = 5000
folder = "../shot_VR/dataset/"
filename = "Tiro_0"

# Read seismic data
seismic = readbinaryfile(Nx,Nt,folder+filename+".bin")

# Read trace header data
traceheadertable = np.loadtxt("../shot_VR/header/Header_tiro0.txt",skiprows=1)


# pl.imshow(seismic.T,aspect="auto")
# pl.show()

# Create a segy from a 2D matrix
segyio.tools.from_array2D(folder+filename+".sgy",seismic)

# read empty segy
SEGY  = segyio.open(folder+filename+".sgy",'r+',ignore_geometry=True)

#get binary header key
binheader = segyio.binfield.keys

del binheader['Unassigned1'] # remove unassigned1 key
del binheader['Unassigned2'] # remove unassigned2 key

# Edit binary header keys
SEGY.bin[segyio.BinField.Interval]              = 100   #3217-3218* Sample interval in microseconds (µs). Mandatory for all data types.
SEGY.bin[segyio.BinField.IntervalOriginal]      = 100   #3219-3220  Sample interval in microseconds (µs) of original field recording.
SEGY.bin[segyio.BinField.Format]                = 1   #3225-3226@ Data sample format code. Mandatory for all data. For ANP - BDEP it has to be = 1
SEGY.bin[segyio.BinField.SortingCode]           = 1   #3229-3230@ Trace sorting code
SEGY.bin[segyio.BinField.MeasurementSystem]     = 1   #3255-3256@ Measurement system: Highly recommended for all types of data. 1 = Meters 2 = Feet
SEGY.bin[segyio.BinField.ImpulseSignalPolarity] = 1   #3257-3258@ Impulse signal polarity 

# print binary header
print("\n Check binary header \n")
print("%25s %4s %5s \n" %("key","byte","value"))
for k,v in binheader.items():    
    print("%25s %d  %d" %(k,v,SEGY.bin[v]))

#trace numbering
tracl = np.arange(1,seismic.shape[0]+1)

# set trace headers values
for idx, key in enumerate(SEGY.header):
      key.update({segyio.TraceField.TRACE_SEQUENCE_LINE            : tracl[idx]              }) #1-4@ Trace sequence number within line (will increase if line continues on another reel) 
      key.update({segyio.TraceField.FieldRecord                    : 1                       }) #9-12*    Original field record number
      key.update({segyio.TraceField.TraceNumber                    : tracl[idx]              }) #13-16*   Trace number within original field record. It should be the field channel numbe
      key.update({segyio.TraceField.CDP                            : tracl[idx]              }) #21-24@   CMP number
      key.update({segyio.TraceField.CDP_TRACE                      : tracl[idx]              }) #25-28    Trace number within the CDP ensemble (each ensemble starts with trace number one)
      key.update({segyio.TraceField.TraceIdentificationCode        : 1                       }) #29-30*   Trace identification code:   
      key.update({segyio.TraceField.offset                         : int(traceheadertable[idx,6]) })   #37-40@   Distance from source point to receiver group  
      key.update({segyio.TraceField.ReceiverGroupElevation         : int(traceheadertable[idx,5]*100) }) #41-44@   Receiver group elevation 
      key.update({segyio.TraceField.SourceSurfaceElevation         : int(traceheadertable[idx,2]*100) }) #45-48@   Surface elevation at source 
      key.update({segyio.TraceField.ElevationScalar                : 100                     })   #69-70@   Scaler to be applied to all elevations and depths specified
      key.update({segyio.TraceField.SourceGroupScalar              : 100                     })   #71-72@   Scaler to be applied to all coordinates specified in bytes 73-88 to give real value.
      key.update({segyio.TraceField.SourceX                        : int(traceheadertable[idx,0]*100)})   #73-76@   Source coordinate X.
      key.update({segyio.TraceField.SourceY                        : int(traceheadertable[idx,1]*100)})   #77-80@   Source coordinate Y.
      key.update({segyio.TraceField.GroupX                         : int(traceheadertable[idx,3]*100)})   #81-84@   Group coordinate X. 
      key.update({segyio.TraceField.GroupY                         : int(traceheadertable[idx,4]*100)})   #85-88@   Group coordinate Y.
      key.update({segyio.TraceField.CoordinateUnits                : 1                       })   #89-90@   Coordinate units. 1= length (meters or feet) 2= seconds of arc
      key.update({segyio.TraceField.TRACE_SAMPLE_INTERVAL          : 100                     })   #117-118@ Sample interval in microseconds for this trace 
      key.update({segyio.TraceField.GainType                       : 1                       })   #119-120  Gain type of field instruments: 
      key.update({segyio.TraceField.TimeBaseCode                   : 1                })   #167-168@ Time basis code: 1=local; 2=GMT; 3=other.
      key.update({segyio.TraceField.CDP_X                          : int(traceheadertable[idx,8]) })   #181-184@ X coordinate for CMP. [I4]
      key.update({segyio.TraceField.CDP_Y                          : int(traceheadertable[idx,9]) })   #185-188@ Y coordinate for CMP. [I4]

# get trace headers key
traceheaders = segyio.tracefield.keys

# print trace header
print("\n Check trace header \n")
print("%40s %5s %6s %6s \n" %("Trace header ","byte","first","last"))
for k,v in traceheaders.items():    
    print("%40s %5d  %6d %6d " %(k,v,SEGY.attributes(v)[0],SEGY.attributes(v)[SEGY.tracecount-1]))

SEGY.close()
