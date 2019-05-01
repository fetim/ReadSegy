#! /bin/sh
# Examples of segyread and segywrite
# Author    : John Stockwell
# Modify by : Felipe Timoteo
set -x
#####
##
## processing steps:
##	1) segyread --- to get ASCII and BINARY tape header files: hfile1
##			bfile1 from beginning of tape
##	2) segyread --- again, now to get full data set from tape, but being 
##	   		careful to output ASCII and BINARY tape headers to
##			to hfile2 and bfile2
##	3) segyclean --	to zero optional segy header fields
##
##	4) Save in Seismic Unix format
##
##  5) Show header information and plot input data (optional)
## additional info: selfdocs of segyread, segyclean, and segywrite

######### USER AREA  #############

path=segy/          #paths with segy data
pathsu=su/
inputfilename=sigsbee2a_nfs_10shots	# raw tape device being read from

######### USER AREA  #############


tape1=$path$inputfilename'.sgy'
outfile=$pathsu$inputfilename'_outfile.su' 	# output filename
tmppath=.tmp/

bfile1=$tmppath'binary1_'$inputfilename  # BINARY header filename 1
hfile1=$tmppath'header1_'$inputfilename  # ASCII header filename 1
bfile2=$tmppath'binary2_'$inputfilename  # BINARY header filename 2
hfile2=$tmppath'header2_'$inputfilename  # ASCII header filename 2
verbose=1		# =1 list more info ;  =0 (default) silent
buff=1			# =1 (default) for 9 trac tape;  =0 for EXABYTE

# first pass of segyread to get binary header
segyread	verbose=$verbose \
		buff=$buff \
		tape=$tape1 \
		bfile=$bfile1 \
		hfile=$hfile1  > /dev/null 

# second pass of segyread to get all desired traces
segyread	verbose=$verbose \
		buff=$buff \
		tape=$tape1 \
		bfile=$bfile2 \
		hfile=$hfile2 | 
segyclean > $outfile


surange < $outfile &

suximage < $outfile perc=99&

# clean trash
cd $tmppath
rm *$inputfilename*
cd ../

exit 0
