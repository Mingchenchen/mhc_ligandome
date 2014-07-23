import sys

import os 
from os import makedirs, listdir
from os.path import join, exists

if __name__ == '__main__':
	assert len(sys.argv) == 2
	source_dir = sys.argv[1]
	if source_dir.endswith("/"):
		source_dir = source_dir[:-1]
	assert exists(source_dir)
        target_dir = source_dir + "_reduced"
	if exists(target_dir):
		os.rmdir(target_dir)
	makedirs(target_dir)
	source_files = listdir(source_dir)

	sizes = {}

	# get file sizes 
	for filename in source_files:
		stat = os.stat(join(source_dir, filename))
		sizes[filename] = stat.st_size

	# map each distinct number of bytes to all files which are of that size
	equiv_sizes = {}
	for (name, size) in sizes.iteritems():
		if size in equiv_sizes:
			equiv_sizes[size].append(name)
		else:
			equiv_sizes[size] = [name]

	print "%d files, %d distinct sizes" % (len(sizes), len(equiv_sizes))
	mappings = {}
	for filename in source_files:
		if filename in mappings:
			print "Skipping", filename 
			continue 
		
		print filename
		mappings[filename] = filename
		
		with open(join(source_dir, filename), 'r') as input_file:
			contents = input_file.read()

		# copy source to destination 
		with open(join(target_dir, filename), 'w') as output_file:
			output_file.write(contents)
		size = sizes[filename]
		# look for identical files and add them to the mappings
		other_filenames = equiv_sizes[size]
		if len(other_filenames) > 1:

			counter = 0
			for other_filename in other_filenames:
				if other_filename != filename:
					with open(join(source_dir, other_filename), 'r') as other_file:
						other_contents = other_file.read()
						same = (contents == other_contents)
						if same:
							mappings[other_filename] = filename
							counter += 1
			print "-- %d / %d identical alleles with same file size" % (counter, len(other_filenames) - 1)
	with open(join(target_dir, "mappings"), 'w') as f:
		for (k,v) in mappings.iteritems():
			f.write("%s\t%s\n" % (k,v)) 

