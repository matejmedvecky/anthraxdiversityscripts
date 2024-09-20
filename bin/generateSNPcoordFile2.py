#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:11:48 2024

@author: mmedvecky
"""

# infile here is alignment table (see anthraxdiversityscripts repo) with 3 columns added to the beginning (chromosome, position, ref allele)

import sys

def generate_SNP_coord_file():
    if len(sys.argv) != 2:
        print("USAGE: %s init_table" % sys.argv[0])
        return False
    
    with open(sys.argv[1], 'r') as infile, open("SNP_coordinates.tsv", 'w') as outfile:
        infile.readline()
        for line in infile:
            data = line.split('\t')
            refAllele = data[2].rstrip()
            outfile.write('%s\t%d\t%s\t' % (data[0], int(data[1]), data[2]))
            isCovered = False
            altAlleles = []
            isFirst = True
            for base in data[3:]:
                if base.rstrip() != refAllele and base.rstrip() != '-' and base.rstrip() != 'N':
                    if altAlleles:
                        if base.rstrip() not in altAlleles:
                            print('\nWARNING: Be aware that at position %d, there are multiple alternate bases detected among cohort of input files.' % int(data[1]))
                            outfile.write('%s\t%d\t%s\t%s\n' % (data[0], int(data[1]), data[2], base.rstrip()))
                            altAlleles.append(base.rstrip())
                    if isFirst:
                        outfile.write('%s\n' % base.rstrip())
                        altAlleles.append(base.rstrip())
                        isFirst = False
                    isCovered = True
            if not isCovered:
                print("\nWARNING: Unable to detect variant allele at position %d\n" % int(data[1]))
                outfile.write('N\n')
            

generate_SNP_coord_file()