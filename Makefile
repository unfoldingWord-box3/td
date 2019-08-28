# Makefile that runs the html generation as a convenience for testing
#

html:
	time make -C docs html
	
default: html
