import segyio
import matplotlib.pyplot as pl
import numpy as np
from segyio_tools import parse_text_header

folder   = "../segy/"
filename = "0212-0019_Amplitudes"

SEGY     = segyio.open(folder+filename+".sgy",ignore_geometry=True)
print("\n Reading segy: %s%s" %(folder,filename))

#get binary header keys
binheader = segyio.binfield.keys

del binheader['Unassigned1'] # remove unassigned1 key
del binheader['Unassigned2'] # remove unassigned2 key

# print binary header
print("\n Check binary header \n")
print("%40s %5s %5s \n" %("key","byte","value"))
for k,v in binheader.items():    
    print("%40s %5d  %5d" %(k,v,SEGY.bin[v]))

# get Text header
text_headers  = parse_text_header(SEGY)
print(' \n \n \n Text Header \n')
for line in text_headers:
    print(line, text_headers[line])

# get trace header keys
traceheaders = segyio.tracefield.keys

# print trace header
print("\n Check trace header \n")
print("%40s %5s %8s %8s \n" %("Trace header ","byte","first","last"))
for k,v in traceheaders.items():    
    print("%40s %5d  %8d %8d " %(k,v,SEGY.attributes(v)[0],SEGY.attributes(v)[SEGY.tracecount-1]))

# pl.plot(SEGY.attributes(223)[int(863*500):int(863*600)])
# pl.show()