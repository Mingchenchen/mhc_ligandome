import sys

import os 
from os import makedirs, listdir
from os.path import join, exists
from collections import Counter
import math

def positional_entropies(peptides):
    assert peptides, "Expected non-empty list"
    n = len(peptides[0])
    assert all(len(p) == n for p in peptides), "All peptides must be of same length"
    
    # create an amino acid counter for each position in the peptide
    counters = []
    for _ in xrange(n):
        counters.append(Counter())
    for p in peptides:
        for i, x in enumerate(p):
            counters[i][x] += 1
    entropies = []
    for i in xrange(n):
        values = counters[i].values()
        denom = sum(values)
        total_entropy = 0.0
        for k,v in counters[i].iteritems():
            prob = float(v) / denom 
            total_entropy -= prob * math.log(prob)
        entropies.append(total_entropy)
    return entropies

if __name__ == '__main__':
    assert len(sys.argv) == 2
    source_dir = sys.argv[1]
    if source_dir.endswith("/"):
        source_dir = source_dir[:-1]
    assert exists(source_dir)
    target_filename = source_dir + "_entropies.csv"
    
    source_files = listdir(source_dir)

    with open(target_filename, 'w') as output_file:
        for source_file in source_files:
            with open(join(source_dir, source_file), 'r') as input_file:
                contents = input_file.read()
            peptides = [l for l in contents.split("\n") if l]
            entropies = positional_entropies(peptides)
            print source_file, entropies
            output_string = source_file + "," + ",".join("%0.4f" % v for v in entropies)
            output_file.write(output_string)
            output_file.write("\n")

