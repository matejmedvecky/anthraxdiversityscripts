# README

This Repo consists of scripts and workflow for the assessment of SNP read mapping metrics data (generated via varscan and bam-readcount tools), variant site filtering and generation of variant call and MSA alignment files

README file provides example of how this set of scripts was used in our *Bacillus anthracis* genomic diversity paper

Please cite the paper and/or URL to this GitHub repo when using them in your work


\# generate SNPs via varscan from BAM files\
\# change /path/to/ to real path to given files/executables in your file system
```bash
for filename in *bam; do samtools mpileup -f /path/to/reference.fasta $filename | java -jar /path/to/VarScan.v2.4.4.jar pileup2snp --min-coverage 4 --min-reads2 2 --min-var-freq 0.95 --min-avg-qual 20 > ${filename%bam}varscan; done
```

\# produce panSNP file by merging all unique SNP positions detected by varscan across all BAM files
```bash
./extractAllSNPs.py /path/to/dir/with/varscan/files
```

\# generate SNP interval file to reduce output of bam-readcount tool
```bash
awk '{printf "%s\t%s\t%s\n", $1, $2, $2}' panSNPs.txt > panSNPs_intervals.txt
```

\# generate read mapping metrics files for SNP sites via bam-readcount
```bash
for filename in *bam; do bam-readcount -w 1 -b 20 -l panSNPs_intervals.txt -f /path/to/reference.fasta $filename > ${filename%bam}bam-readcount; done
```

\# generate variant call table (tab-delimited)\
\# you may generate panSNP.txt file by script 'generate_SNPfile.py' - see commented lines in that script for input clarification\
\# format of the table is explained below
```bash
./makeVCtable.py panSNPs.txt /path/to/dir/with/bam-readcount/files
```

\# optionally, generate variant call table (tab-delimited) with monomorphic sites excluded (those are outputted in separate text file)\
\# site is considered as monomorphic if all investigated isolates possess the same base at given position that differs from the reference
```bash
./makeVCtableNoMonomorphic.py VC_table.dat
```

\# generate variant call flag table\
\# user must specify coverage threshold and base frequency threshold - flags are risen in sites that are below specified thresholds
```bash
./makeVCflagTable.py VC_table.dat 4 0.89
```

\# at this stage, user can refine the dataset by removing sites or samples with too many flags\
\# we also removed sites from phages and homologous regions\
\# e.g. awk commands to filter out or output all sites with 2 and more flags:
```bash
awk -F 'below' '{if (NF-1 < 2) {print $0}}' VC_flag_table.dat > VC_flag_table_refined.dat
awk -F 'below' '{if (NF-1 >= 2) {print $0}}' VC_flag_table.dat > VC_flag_table_problematic_sites.dat
```
\# user can use script removeSelectedRegions.py for automatic removal of sites with too many flags\
\# first, generate file with problematic intervals (tab-delimited file with starting and ending positions), e.g.:
```bash
awk '{printf "%s\t%s\n",$2,$2}' VC_flag_table_problematic_sites.dat > VC_flag_table_problematic_sites_intervals.txt
```
\# execute script afterwards
```bash
./removeSelectedRegions.py VC_table.dat VC_flag_table_problematic_sites_intervals.txt 
```

\# generate alignment table (tab-delimited)\
\# user must specify coverage threshold and base frequency threshold - sites below coverage threshold are represented as ‘-‘ and sites below frequency threshold are represented as ’N’ in the alignment table
```bash
./generateAlignmentTable.py VC_table_refined.dat 4 0.89
```

\# user can also add outgroup to alignment table (e.g. by copying ref allele column from refined VC table)

\# transpose table in MS Excel or LibreOffice Calc

\# generate final FASTA alignment file by following awk command
```bash
awk '{printf (">%s\n",$1); for (i=2; i<=NF; i++) printf ("%s",$i); printf ("\n")}' alignment_table_transposed.txt > alignment_file.afa
```


\# explatanion of variant call table
```
chromosome	position	ref allele	AN16-110_S	AN16-24_S2
NC_007530_Bacillus_anthracis_Ames_Ancestor	17294	T	C:316(160,156):2(1,1)/314(159,155)/0(0,0)/0(0,0)/0(0,0)/0	C:83(42,41):0(0,0)/83(42,41)/0(0,0)/0(0,0)/0(0,0)/0
NC_007530_Bacillus_anthracis_Ames_Ancestor	359536	G	A:101(50,51):101(50,51)/0(0,0)/0(0,0)/0(0,0)/0(0,0)/0	A:27(13,14):27(13,14)/0(0,0)/0(0,0)/0(0,0)/0(0,0)/0
```

\# each line consist of reference chromosome, position of SNP, reference allele and read metrics for each sample\
\# read metrics has following format: prevalent base: total number of mapped reads(forward,reverse): number of reads with A(forward,reverse)/number of reads with C(forward,reverse)/number of reads with G(forward,reverse)/number of reads with T(forward,reverse)/number of reads with N(forward,reverse)/number of indel reads\
\# if more than 50% of mapped reads have indel at given site, there is keyword INDEL as prevalent base\
\# if there are two prevalent bases with the same coverage, there is keyword AMBIGUOUS as prevalent base
