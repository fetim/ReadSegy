#! /bin/sh
# Examples of sort
# Author    : Felipe Timoteo
set -x
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
## 

######### USER AREA  #############

path=segy/          #paths with segy data
pathsu=su/
inputfilename=Norte_outfile	# raw tape device being read from

######### USER AREA  #############

tmppath=.tmp/
indata=$pathsu$inputfilename'.su'


suximage < $indata perc=99 &

surange < $indata

susort < $indata tracl ep | suximage perc=99 &