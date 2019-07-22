# reference-panel-reconstruction
This is an easily-to-use tool for users to reconstruct imputation reference panels of 1000G, and to investigate the imputation accuracy changes pattern for a particular population of interest. Note that the Bcftools and Minimac3 are required.

Use the follow command to download: 

  	sudo git clone https://github.com/Abyss-bai/reference-panel-reconstruction.git

Please run the follow command to check the helpdoc first:

	python ./reference_panel_re-construction.py -H

And this will output a flag list, User can set the study population, diverse populations, step size and adding times with these flags:
 	
 	-H/-h	Show this help doc.  
	
	-P	The three-uppercase-letter abbreviation 
		of 1000G population that specific to the 
		GWAS set. This population will be the 
		basic panel.
	
	-S	The sample file of 1000G reference panel.
	
	[-I]	Specify the populations of 1000G as 
		the diversity parts to the basic 
		panel. Please use the three-uppercase-letter 
		abbreviations and separated each population 
		by commas and without blank space. The 
		defult value is eight populations that are 
		randomly selected from four diverse 1000G 
		groups (to the basic panel), each group 
		contains two.
	
	[-T]	The diversity-samples-adding (recursively) 
		times. The defult value is twelve.
 
An example.sh file is given, and this will output a series file of sample ID of 1000G and a "Imputation_Template.sh" script. The sample ID files correspond to the composition of new reference panels. For the next reference panel contruction and imputation, please follow the instruction in Imputation_Template.sh and modify it. 
