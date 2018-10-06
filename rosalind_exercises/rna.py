import sys

dna_string = sys.argv[1]

rna_string = ''

for base in dna_string:
    if base == 'T': base = 'U'
    rna_string += base

print(rna_string)