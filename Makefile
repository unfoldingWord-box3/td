# Makefile that runs the html generation as a convenience for testing
#

html:
	python3 bin/dataprep.py
	make -C docs html
	
default: html
