#!/usr/bin/env python

import yaml
import sys
import operator
import itertools
import pickle
import pprint

if len(sys.argv) == 2 :
	source = sys.argv[1]		# '.yml' file as input file
else:
	source = 'sources.yml'		# Default .yml file


yfile = yaml.load(open(source))		

# Extracting languages mentioned in '.yml' file and assiging each a label in the process
label = dict()
count = 0
for i in yfile:
	label[i] = count
	count += 1

finalLabel = sorted(label.items(), key=operator.itemgetter(1))


# Saving the generated label in '.pickle' file in binary format
with open('genearatedLabels.pickle', 'wb') as handle:
    pickle.dump(finalLabel, handle, protocol=pickle.HIGHEST_PROTOCOL)

print "\n* LABELS GENERATED IN BINARY FORMAT AS 'genearatedLabels.pickle' *\n"

y = raw_input("To view generated labels (press Enter) :")

if y == "":
	for i in finalLabel :
		print "\n"
		print i
