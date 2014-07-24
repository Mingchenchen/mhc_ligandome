import sys

import os 
from os import makedirs, listdir
from os.path import join, exists, split
import glob 
from collections import Counter 

import argparse

parser = argparse.ArgumentParser(description='Transform ligand set by extracting substring of each peptide')

parser.add_argument('source_dir', help="Input directory of full ligandome peptides")

parser.add_argument('--start', type=int, default = 3,
                   help='Start position (from 1 to 9)')

parser.add_argument('--stop', type=int, default = 8,
                   help='Stop position (from 1 to 9, inclusive)')


if __name__ == '__main__':

	args = parser.parse_args()
	source_dir = args.source_dir
	if source_dir.endswith("/"):
		source_dir = source_dir[:-1]
	assert exists(source_dir)
	target_dir = source_dir + "_positions_%d_%d" % (args.start, args.stop)   
	if exists(target_dir):
		os.rmdir(target_dir)
	makedirs(target_dir)
	
	source_files = listdir(source_dir)
	
	for filename in source_files:
		with open(join(source_dir, filename), 'r') as input_file:
			contents = input_file.read()

		with open(join(target_dir, filename), 'w') as output_file:
			if not (filename.startswith("A") or filename.startswith("B") or filename.startswith("C")):
				output_file.write(contents)
			else:
				start = args.start - 1 
				stop = args.stop
				substrings = set([])
				counter = 0
				for peptide in contents.split("\n"):
					if len(peptide) > 0:
						substrings.add(peptide[start:stop])
						counter += 1 
				print "%s: total = %d, unique = %d" % (filename, counter, len(substrings))
				for substring in sorted(substrings):
					output_file.write(substring)
					output_file.write("\n")