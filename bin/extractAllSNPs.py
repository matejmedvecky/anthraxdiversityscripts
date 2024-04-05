#!/usr/bin/python

#created by Matej Medvecky

import re
import sys
import glob


def extract_SNPs():
	if len(sys.argv) != 2:
		print('USAGE: %s /path/to/dir/with/varscan/files' % sys.argv[0])
		return False

	positionPattern = re.compile(r'(.+?)\t(\d+?)\t(.)\t.+')# reference contig, position, reference base
	SNPs = []
	for filename in glob.glob(sys.argv[1] + '/*varscan'):
		inFile = open(filename, 'r')
		for line in inFile:
			snpData = positionPattern.findall(line)
			isInSNPs = False
			if snpData:
				for snp in SNPs:
					if snpData[0][0] == snp[0]:
						if int(snpData[0][1]) == snp[1]:
							isInSNPs = True
							break
				if not isInSNPs:
					SNPs.append([snpData[0][0], int(snpData[0][1]), snpData[0][2]])
		inFile.close()
	SNPs.sort(key=lambda x: x[1], reverse=False)

	outFile = open('panSNPs.txt', 'w')
	for snp in SNPs:
		outFile.write("%s\t%s\t%s\n" % (str(snp[0]), str(snp[1]), str(snp[2])))
	outFile.close()
extract_SNPs()
