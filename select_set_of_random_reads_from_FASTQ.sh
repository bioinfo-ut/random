#!/bin/bash
# Created by Maido Remm, inspired by Pierre Lindenbaum from BioStar forum (https://www.biostars.org/p/6544/#76380) 
# Randomly selects 10**0 to 10**6 reads from FASTQ file, 3 independent variants 


for i in {1..3}
do
   for j in {0..6}
   do
      echo "Output: test.$i.$j.fastq"
      echo $((10**$j))
      cat S.aur_SRR5415283.fastq | awk '{ printf("%s",$0); n++; if(n%4==0) { printf("\n");} else { printf("\t\t");} }' | shuf | head -n $((10**$j)) | sed 's/\t\t/\n/g' > tmp
      cat tmp bacterial_background.fastq > test_nohs.$i.$j.fastq
      rm -f tmp
   done
done