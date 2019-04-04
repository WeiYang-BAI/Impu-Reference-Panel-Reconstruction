import re
import sys
import random

def getArgvDict(argv):
		optionDict = {}
		c = 0
		for i in argv:
				if re.match('-', i):
						optionDict[i] = argv[c + 1]
				c += 1
		return optionDict

def selectPopulation(mainPop):
		pops = []
		for i in OKG:
				if mainPop not in i:
						tmp = random.sample(i, 2)
						pops.extend(tmp)
		return pops

def selectSample(mainPop, divPops, okgSample, addTimes):
		try:
				with open(okgSample, 'r') as f:
						allSample = f.read()
		except IOError as e:
				print(e)
				sys.exit()
		else:
				baseSample = re.findall(r'(\w+)\s'+mainPop+'\s\w+\s', allSample)
				baseSample = [i + "\n" for i in baseSample]
		for p in divPops:
				tmp = random.sample(re.findall(r'(\w+)\s'+p+'\s\w+\s', allSample), int(addTimes))
				tmp = [i + "\n" for i in tmp]
				for n in range(int(addTimes)+1):
						if p == divPops[0]:
								bT = open('Panel_with_addtions_' + str(n) + '.sample', 'w')
								bT.writelines(baseSample)
								bT.close()
						dT = open('Panel_with_addtions_' + str(n) + '.sample', 'a')
						for m in range(n):
								dT.write(tmp[m])
						dT.close()

if __name__ == '__main__':
		AMR = ['MXL', 'PUR', 'CLM', 'PEL']
		EAS = ['CHB', 'JPT', 'CHS', 'CDX', 'KHV']
		EUR = ['CEU', 'TSI', 'FIN', 'GBR', 'IBS']
		SAS = ['GIH', 'PJL', 'BEB', 'STU', 'ITU']
		AFR = ['YRI', 'LWK', 'GWD', 'MSL', 'ESN', 'ASW', 'ACB']
		OKG = [EAS, EUR, AFR, AMR, SAS]
		helpDoc = '''
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
		'''
		argv = sys.argv
		if re.search('-H|-h', str(argv)):
				print(helpDoc)
				sys.exit()
		try:
				envDict = getArgvDict(argv)
				mainPop = envDict['-P']
				okgSample = envDict['-S']
		except KeyError as e:
				print('ERROR: Incomplete or invalid arg '+str(e)+' ! Please check your input, or use -H/-h flag to get help.')
				sys.exit()
		else:
				divPops = (envDict['-I'].split(',') if envDict.get('-I') else selectPopulation(mainPop))
				addTimes = (envDict['-T'] if envDict.get('-T') else '12')
		selectSample(mainPop, divPops, okgSample, addTimes)
		imT = open('Imputation_Template.sh','w')
		imT.write('''
#!/bin/sh

# In order to reduce the computation load, only chromosome 2 
# will be imputed in this script. All parameters could be  
# modified based on actual demand. Besides, please replace all 
# the file paths and filenames at '/your-path/...' positions 
# by the real ones.

for i in $(seq 0 '''+ str(addTimes) +'''); do
/your-path/bcftools \\
	view -Ov \\
	--samples-file ./Panel_with_addtions_${i}.sample \\
	/your-path/The-1000G-reference-panel-chr2.vcf \\
	--output-file /your-path/New-reference-panel-chr2.vcf

/your-path/Minimac3-omp \\
	--refHaps /your-path/New-reference-panel-chr2.vcf \\
	--processReference \\
	--prefix /your-path/New-reference-panel-in-m3vcfFormat-chr2 \\
	--cpus 24

/your-path/Minimac3-omp \\
	--refHaps /your-path/New-reference-panel-in-m3vcfFormat-chr2.m3vcf.gz \\
	--haps /your-path/The-study-data-QCed-phased-chr2.vcf \\
	--prefix /your-path/Imputation-Result-chr2 \\
	--chr 2 \\
	--rounds 5 \\
	--states 200 \\
	--cpus 24 \\
	--params
done
''')
		imT.close
		print('Done, ' + str(addTimes) + ' new reference panel sample sets were formed in total, and corresponding to the files "Panel_with_addtions_0-' + str(addTimes) + '.sample". For reference panel re-construction and imputation, please refer to the "Imputation_Template.sh" file.')