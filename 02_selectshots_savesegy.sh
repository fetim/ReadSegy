#! /bin/sh
# Examples of suwind and segywrite
# Author: Felipe Timóteo
set -x
##
## processing steps:
##	1) read seismic unix data and show input data (optional)
##	
##	2) Select key and define the range 
##
##  3) extract header from seismic unix file
##	
##	4) Apply the window
##	
##	5) write in segy format
## additional info: selfdocs of segyread, su	wind, segyhdrs, and segywrite

######### USER AREA  #############

path=segy/  
pathsu=su/
inputfilename=sigsbee2a_nfs_outfile

key=fldr  # key used to windowing data
min=0    # lower limit
max=10   # upper limit

######### USER AREA  #############

tmppath=.tmp/
bfile=$tmppath'binary_'$inputfilename		# BINARY header filename
hfile=$tmppath'header_'$inputfilename		# ASCII header filename
verbose=1		# =1 list more info ;  =0 (default) silent
buff=1			# =1 (default) for 9 trac tape;  =0 for EXABYTE

indata=$pathsu$inputfilename'.su'
tape=$path$inputfilename'_key-'$key'_min-'$min'_max-'$max'.sgy'


# Don't recommended for large data set
#suximage < $indata perc=99 &

# windowing input data
suwind < $indata    \
         key=$key   \
         min=$min   \
         max=$max > $tmppath'tmp.su'

# extracting header
segyhdrs < $tmppath'tmp.su' 

# adjusting names
mv header $hfile
mv binary $bfile

# Write in segy
segywrite 	verbose=$verbose \
		 buff=$buff \
		 tape=$tape \
		 bfile=$bfile \
		 hfile=$hfile < $tmppath'tmp.su'


# Check output range
suximage < $tmppath'tmp.su' perc=99 &
surange < $tmppath'tmp.su' &

# clean trash
cd $tmppath
rm *$inputfilename* *.su
cd ../

exit 0


