#!/bin/sh

# To get helpdoc with '-H' flag.
python \
	./reference_panel_re-construction.py \
	-P CHB \
	-S ./1000GP_Phase3.sample \
	-I MXL,CEU,PJL,GWD,ITU,GBR \
	-T 8
