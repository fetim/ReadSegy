#! /bin/sh
# Examples of sort
# Author    : Felipe Timoteo

#####
##
## processing steps:
##	1) Read seismic unix data
##   
##	2)
##	 
##	3)
##               
##	4)
##                                 
##  5)
## additional info: selfdocs of susort

######### USER AREA  #############

path=segy/          #paths with segy data
pathsu=su/
inputfilename=sigsbee2a_nfs_10shots_outfile	# raw tape device being read from

######### USER AREA  #############

tmppath=.tmp/
indata=$pathsu$inputfilename'.su'


suximage < $indata perc=99 &

surange < $indata

susort < $indata cdp offset | suximage perc=99 &
