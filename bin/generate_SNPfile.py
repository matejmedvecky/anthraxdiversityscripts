#!/usr/bin/env python

import re
import sys
import traceback
from Bio import SeqIO


#created by Matej Medvecky

#This script can be used to generate panSNPs.txt file which is a required parameter for makeVCtable.py
#Fasta file should be your reference. File with SNP positions should contain one SNP position per line consisting of reference header and position of SNP delimited by tab. First base has position 1.
#biopython is a dependency here. You may install it by command "pip install biopython" or "pip3 install biopython".

def make_SNPfile():
    if len(sys.argv) != 4:
        sys.stderr.write('Error: Incorrect number of arguments.\n'\
            'USAGE: %s </path/to/input/fasta/file> </path/to/input/file/with/SNP/positions> <output_filename>' % sys.argv[0])
        return False

    try:
        with open(sys.argv[1], 'r') as inFaFile, open(sys.argv[2], 'r') as inSnpFile, open(sys.argv[3], 'w') as outFile:
            for line in inSnpFile:
                inFaFile.seek(0)
                for record in SeqIO.parse(inFaFile, "fasta"):
                    if record.id == str(line.rstrip().split()[0]):
                        outFile.write("%s\t%s\t%s\n" % (str(line.rstrip().split()[0]), str(line.rstrip().split()[1]), record.seq[int(line.rstrip().split()[1])-1]))
    except IOError:
        sys.stderr.write('Error: Problem with input/output files.\n')
        traceback.print_exc()
        return False
    except:
        sys.stderr.write('Error: Something went wrong.\n')
        traceback.print_exc()
        return False

make_SNPfile()
