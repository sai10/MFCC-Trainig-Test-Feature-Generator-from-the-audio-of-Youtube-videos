# -*- coding: utf-8 -*-

import sys
import os
import fnmatch
import math
import itertools
from random import shuffle
import pickle

if len(sys.argv) == 3 :
	source = sys.argv[1]
	dest = sys.argv[2]
	th = int(sys.argv[3])
else:
	source = 'input/segmented/' 	# default input destination
	dest = 'output/'		# default output destination		
	th = 0.8			# default train validation split

root_dir = os.getcwd()			# root directory


def recursive_glob(path, pattern):	# For listing all folders and files based on pattern recursively of the path provided
    for root, dirs, files in os.walk(path):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.abspath(os.path.join(root, basename))
                if os.path.isfile(filename):
                    yield filename

def get_immediate_subdirectories(path):	# Finding out the subdirectories of the path provided
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

languages = sorted(get_immediate_subdirectories(source))


#######################################################
# loading of labels from 'genearatedLabels.pickle' file
#######################################################
def Convert2dict(tup, di):
    di = dict(tup)
    return di

with open('genearatedLabels.pickle', 'rb') as handle:
	tmpLABELS = pickle.load(handle)

LABELS = dict()
LABELS = Convert2dict(tmpLABELS, LABELS)


###################################
# Count all files for each language
###################################
counter = dict()				# To store number of files under each language 
file_names = dict()				# To store name of files under each language

for lang in languages:
        #print(lang)
        files = list(recursive_glob(os.path.join(source, lang), "*.wav"))
        files.extend(recursive_glob(os.path.join(dest, lang), "*.png"))
        num_files = len(files)
        file_names[lang] = files
        counter[lang] = num_files


####################################
# Calculate train / validation split
####################################


smallest_count = min(counter.values())
#print smallest_count
num_test = int(smallest_count * 0.1)				# Number of test cases
#print num_test
num_train = int(smallest_count * (th - 0.1))			# Number of train cases 
#print num_train
num_validation = smallest_count - num_train - num_test		# Number of validation cases
#print num_validation

# Split datasets and shuffle languages
training_set = []
validation_set = []
test_set = []

for lang in languages:
    label = LABELS[lang]
    training_set += zip(file_names[lang][:num_train], itertools.repeat(label))
    validation_set += zip(file_names[lang][num_train:num_train + num_validation], itertools.repeat(label))
    test_set += zip(file_names[lang][num_train + num_validation:num_train + num_validation + num_test], itertools.repeat(label))

shuffle(training_set)
shuffle(validation_set)
shuffle(test_set)


##############
# Write to CSV
##############

train_file = open(os.path.join(root_dir, "training.csv"), "w")			# Training File
validation_file = open(os.path.join(root_dir, "validation.csv"), "w")		# Validation File
test_file = open(os.path.join(root_dir, "testing.csv"), "w")			# Testing File 

for (filename, label) in training_set:
        train_file.write("{}, {}\n".format(filename, label))

for (filename, label) in validation_set:
        validation_file.write("{}, {}\n".format(filename, label))

for (filename, label) in test_set:
        test_file.write("{}, {}\n".format(filename, label))

train_file.close()
validation_file.close()
test_file.close()

############
# Statistics
############
print("[Training]   Files per language: {} Total: {}".format(num_train, num_train * len(languages)))
print("[Validation] Files per language: {} Total: {}".format(num_validation, num_validation * len(languages)))
print("[Testing]    Files per language: {} Total: {}".format(num_test, num_test * len(languages)))

