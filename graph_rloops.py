from __future__ import division
import sys
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy.stats as st
import numpy as np
import random

infile = open(sys.argv[1],'r')
infile2 = open(sys.argv[2],'r')

#variables
probability = []
energy = []

#process the model_infile (fixedStep)
lines = infile.readlines()
header = lines[1].strip().split()
print header[2]
start_loci = int(header[2].split(':')[1].split('-')[0])
#end_loci = int(header[2].split(':')[1].split('-')[1])
#read the fixedStep data
for item in lines[4:]:
	probability.append(float(item))

#process the model_infile (fixedStep)
lines = infile2.readlines()
header = lines[1].strip().split()
print header[2]
start_loci = int(header[2].split(':')[1].split('-')[0])
#end_loci = int(header[2].split(':')[1].split('-')[1])
#read the fixedStep data
for item in lines[4:]:
	energy.append(float(item))

#output both signals to a graph
with PdfPages(sys.argv[3]+'.pdf') as pdf:
	#plt.xlim(-0.14,0.00)
	plt.title('---')
	plt.subplot(2,1,1)
	plt.ylim(0,1)
	plt.xlabel('Position (bp)')
	plt.ylabel('P(x)')
	plt.plot(xrange(len(probability)),probability)
	plt.subplot(2,1,2)
	plt.plot(xrange(len(energy)),energy)
	plt.xlabel('Position (bp)')
	plt.ylabel('Local Avg G(x)')
	plt.subplots_adjust(top=0.92, bottom=0.1, left=0.10, right=0.95, hspace=0.25, wspace=1.8)
	#plt.grid(which='both')
	#plt.ylim((-0.01,1))
	pdf.savefig()
	plt.close()
