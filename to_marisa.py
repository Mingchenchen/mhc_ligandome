import sys

import os 
from os import makedirs, listdir
from os.path import join, exists
from marisa_trie import Trie 

if __name__ == '__main__':
	assert len(sys.argv) == 2
	source_dir = sys.argv[1]
	if source_dir.endswith("/"):
		source_dir = source_dir[:-1]
	assert exists(source_dir)
        target_dir = source_dir + "_marisa"
	if exists(target_dir):
		os.rmdir(target_dir)
	
	makedirs(target_dir)
	source_files = listdir(source_dir)


	for filename in source_files:
		with open(join(source_dir, filename), 'r') as input_file:
			contents = input_file.read()
			
			if filename == 'mappings':
				with open(join(target_dir, 'mappings'), 'w'):
					# copy source to destination 
					output_file.write(contents)
			else:
				print filename 
				with open(join(target_dir, filename + ".marisa"), 'w') as output_file:
					lines = contents.split("\n")
					d = Trie(l for l in lines if len(l) > 0)
					d.write(output_file)
