import sys
from os import makedirs, listdir 
from os.path import join, exists

if __name__ == '__main__':
	assert len(sys.argv) == 2
	source_dir = sys.argv[1]
	if source_dir.endswith("/"):
		source_dir = source_dir[:-1]
	assert exists(source_dir)
        target_dir = source_dir + "_no_ic50"
	assert not exists(target_dir)
	makedirs(target_dir)
	source_files = listdir(source_dir)
	for filename in source_files:
		print filename
		with open(join(source_dir, filename), 'r') as input_file:
			with open(join(target_dir, filename), 'w') as output_file:
				s = input_file.read()
				for i, line in enumerate(s.split('\n')):
					if len(line) > 0:
						peptide = line.split("\t")[0]
						output_file.write(peptide)
						output_file.write("\n")
				print "-- ", i
