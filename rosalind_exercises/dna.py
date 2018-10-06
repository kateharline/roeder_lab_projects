import sys

dna_string = sys.argv[1]

counts = {'A':0, 'C':0, 'G':0, 'T':0}

for base in dna_string:
    counts[base] += 1

print(str(counts['A'])+' '+str(counts['C'])+' '+str(counts['G'])+' '+str(counts['T'])+' ')