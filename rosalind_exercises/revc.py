import sys

dna_strand = sys.argv[1]

dna_reverse = dna_strand[::-1]

complement = {'A':'T', 'C':'G', 'G':'C', 'T':'A'}

rev_comp = [complement[base] for base in dna_reverse]

print(''.join(rev_comp))