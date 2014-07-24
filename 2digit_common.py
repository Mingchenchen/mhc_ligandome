import sys

import os 
from os import makedirs, listdir
from os.path import join, exists, split
import glob 

if __name__ == '__main__':
	assert len(sys.argv) == 2
	source_dir = sys.argv[1]
	if source_dir.endswith("/"):
		source_dir = source_dir[:-1]
	assert exists(source_dir)
	target_dir = source_dir + "_2digit"
	if exists(target_dir):
		os.rmdir(target_dir)
	
	makedirs(target_dir)
	source_files = listdir(source_dir)
	prefixes = set([])
	for filename in source_files:
		if filename.startswith("mapping"):
			with open(join(source_dir, filename), 'r') as in_file:
				with open(join(target_dir, filename), 'w') as out_file:
					out_file.write(in_file.read())
		else:
			prefix = filename[:3]
			prefixes.add(prefix)
	for prefix in sorted(prefixes):
		
		
		family = glob.glob(join(source_dir, "%s*" % prefix))
		
		print prefix, len(family), "alleles"

		peptide_sets = {}
		for allele_path in family:
			with open(allele_path, 'r') as f:
				contents = f.read()
				peptide_set = set(l for l in contents.splitlines() if len(l) > 0)
				peptide_sets[allele_path] = peptide_set
		
		print "-- # alleles", len(peptide_sets)
		common = set.intersection(*peptide_sets.values())
		print "-- Intersection: ", len(common)
		with open(join(target_dir, prefix), 'w') as f:
			for peptide in sorted(common):
				f.write(peptide)
				f.write("\n")

 		for allele_path_input in family:
			allele = split(allele_path_input)[1]
			allele_path_output = join(target_dir, allele)
			with open(allele_path_output, 'w') as f:
				allele_peptide_set = peptide_sets[allele_path_input]
				residual = allele_peptide_set.difference(common)
				n_residual = len(residual)
				n_total = len(allele_peptide_set)
				print "--- %s: %d / %d (%0.4f)" % (allele, n_residual, n_total, float(n_residual) / n_total)
				for peptide in sorted(residual):
					f.write(peptide)
					f.write("\n")
