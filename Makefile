# Makefile that runs the html generation as a convenience for testing
#

html:
	#time python3 bin/dataprep.py
	echo `date`
	time make -C docs html
	echo `date`
	
default: html
