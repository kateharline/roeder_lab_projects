import urllib.request, urllib.parse
import sys
import regex

import singlestring as ss

uniprots = ss.main()
print(uniprots)

def head_parse(response):
    '''
    convert url response into usable protein sequence
    :param response: url data
    :return: protein sequence
    '''
    new_lines = response.split('\n')
    clean_sequence = ''.join(new_lines[1:])

    return clean_sequence


def get_motifs(url, prot):

    # load fasta data
    with urllib.request.urlopen(url) as r:
        response = r.read()

    fasta = head_parse(response.decode())

    # check for motifs using regex N not P s or t not p
    motif = regex.compile('N[^P][ST][^P]')

    starts = []

    for m in motif.finditer(fasta, overlapped=True):
        starts.append(m.start()+1)

    # check for matches
    if starts:
        print(prot)
        print(' '.join(map(str, starts)))



for prot in uniprots:
    url = 'http://www.uniprot.org/uniprot/' + prot + '.fasta'

    get_motifs(url, prot)

