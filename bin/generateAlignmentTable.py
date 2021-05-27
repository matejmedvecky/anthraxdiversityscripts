#!/usr/bin/env python

#created by Matej Medvecky

#VC_table.dat must be tab-delimited table generated by either makeVCtable.py or makeVCtableNoMonomorphic.py

import sys
import re

def make_align_table():
    if len(sys.argv) != 4:
        print("USAGE: %s <VC_table.dat> <coverage_threshold> <frequency threshold>\nCAUTION: Coverage threshold must be an integer value.\nCAUTION: Frequency threshold must be flat lower that 1.0. (e.g. frequency of 20%% must be input as 0.2)." % sys.argv[0])
        return False

    with open(sys.argv[1], 'r') as snpFile, open('alignment_table.dat', 'w') as outFile:
        if float(sys.argv[3]) > 1.0:
            print("ERROR: Frequency threshold is higher than 1.0 (i.e. 100%).")
            return False
        else:
            freqThreshold = float(sys.argv[3])
        headerPattern = re.compile(r'^chromosome\tposition\tref allele\t(.+?)\n')
        headerData = headerPattern.findall(snpFile.readline())
        if not headerData:
            print("ERROR: Correct header is missing! Are you sure you input table generated by makeVCtable.py script?")
            return False
        else:
            outFile.write("%s\n" % headerData[0])
        snps = []
        sitePattern = re.compile(r'.+?\t.+?\t.+?\t(.+?)\n')
        for line in snpFile:
            siteData = sitePattern.findall(line)
            if siteData:
                snps.append(list(siteData[0].rstrip().split("\t")))
            else:
                print("ERROR: Wrong table format! Are you sure you input table generated by makeVCtable.py script?")
                return False

        snpPattern = re.compile(r'^(.+?):(\d+)\(.+?:(\d+)\(.+?\/(\d+)\(.+?\/(\d+)\(.+?\/(\d+)\(.+')
        for snp in snps:
            isFirst = True
            for currSample in snp:
                snpData = snpPattern.findall(currSample)
                if snpData:
                    if isFirst:
                        isFirst = False
                    else:
                        outFile.write("\t")
                    if int(snpData[0][1]) < int(sys.argv[2]):
                        outFile.write("-")
                    elif str(snpData[0][0]) == 'A':
                        if int(snpData[0][1]) > 0 and (float(snpData[0][2])/int(snpData[0][1])) < freqThreshold:
                            outFile.write("N")
                        else:
                            outFile.write("A")
                    elif str(snpData[0][0]) is 'C':
                        if int(snpData[0][1]) > 0 and (float(snpData[0][3])/int(snpData[0][1])) < freqThreshold:
                            outFile.write("N")
                        else:
                            outFile.write("C")
                    elif str(snpData[0][0])== 'G':
                        if int(snpData[0][1]) > 0 and (float(snpData[0][4])/int(snpData[0][1])) < freqThreshold:
                            outFile.write("N")
                        else:
                            outFile.write("G")
                    elif str(snpData[0][0]) == 'T':
                        if int(snpData[0][1]) > 0 and (float(snpData[0][5])/int(snpData[0][1])) < freqThreshold:
                            outFile.write("N")
                        else:
                            outFile.write("T")
                    elif str(snpData[0][0]) == "AMBIGUOUS":
                        outFile.write("N")
                else:
                    print("ERROR: Wrong snp format! Are you sure you input table generated by makeVCtable.py script?")
                    return False
            outFile.write("\n")
make_align_table()
