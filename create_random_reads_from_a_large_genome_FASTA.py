#!/usr/bin/python
# Authors: Marten Rikberg and Maido Remm, 2025
# This script creates random reads in FASTQ format, 
# given contigs from a a large eukaryotic genome sequence in FASTA format


import random
from io import StringIO

read_length = 133
number_of_reads = 100000
number_of_lines = 100000
#infile = open("GCA_031308135.1_ado_dt_MfTpo_fix_genomic.fna")
infile = open("GCA_014858955.1_NU_Adom_1.1_genomic.fna")
outfile = open('acheta.fastq', 'w')

# 1. Read FASTA and join into a single string 
modified_sequence = ""
buf = StringIO()
line_counter = 1
seq_counter = 1

for line in infile:
    line_counter += 1
    if line_counter == number_of_lines:
        break
    if line.startswith(">"):
        seq_counter += 1
        buf.write('*')
    else:
        buf.write(line.strip())
    if line_counter % 1000 == 0:
        print(line_counter, seq_counter, len(buf.getvalue()))

modified_sequence = buf.getvalue()
sequence_length = len(modified_sequence)

# 2. Generate reads
for x in range(number_of_reads):

    # 3. Choose a random position from the string 
    random_pos = random.randrange(0, sequence_length - read_length)
    while "*" in modified_sequence[random_pos:random_pos + read_length]:
        print("Tärn leitud lõigus, valin uue positsiooni.")
        random_pos = random.randrange(0, sequence_length - read_length)

    print("Valitud positsioon:", random_pos)
    end_pos = random_pos + read_length

    # 4. Choose randomly either upper or lower strand 
    random_choice = random.randint(0, 1)
    if random_choice == 0:
        selected_segment = modified_sequence[random_pos:end_pos].upper()
        print("Upper strand fw:", selected_segment)
    else:
        selected_segment = modified_sequence[random_pos:end_pos][::-1].upper()
        selected_segment = selected_segment.replace("A", "t").replace("C", "g").replace("T", "a").replace("G", "c")
        selected_segment = selected_segment.upper()
        print("Lower strand rc:", selected_segment)
    

    # 5. Write the read into FASTQ file
    if random_choice == 0:
        outfile.write("@F" + str(x) + "_" + str(random_pos) + ":" + str(end_pos) + "\n")
    else:
        outfile.write("@R" + str(x) + "_" + str(end_pos) + ":" + str(random_pos) + "\n")
    outfile.write(selected_segment + "\n")
    outfile.write("+\n")
    outfile.write("I" * read_length + "\n")
    