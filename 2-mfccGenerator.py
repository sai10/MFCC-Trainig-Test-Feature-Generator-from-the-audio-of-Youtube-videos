import sys
import os
import matplotlib.pyplot as plt, librosa, librosa.display

'''
(!!* IMP *!!)	NOTE :- Source folder is mandatory for the code to run   <DEPENDENCY ALERT>
'''

# Note in python2 eg. path = 'output' but in python3 path = 'output/' else error will be there 
if len(sys.argv) == 3 :
	source = sys.argv[1]				# Source folder for languages
	dest = sys.argv[2]				# Destination folder for languages
elif len(sys.argv) == 2 :				
	source = sys.argv[1]				# Source folder for languages
	dest = 'output/'				# Default Destination
else:
	source = 'input/segmented/'			# Default Source
	dest = 'output/'				# Default Destination

if os.path.exists(source) == 0 and os.path.exists(dest) == 1 :
	print('Source directory not found')
	sys.exit(0)
elif os.path.exists(dest) == 0 and os.path.exists(source) == 1:
	print('Destination directory not found , so it is now created')
	os.mkdir(dest)
elif os.path.exists(source) == 0 or os.path.exists(dest) == 0 :
	print('Source and Destination directories not found')
	sys.exit(0)


# loading names of language folders from source and creating language folders in destination
listDir = sorted(os.listdir(source))
for i in listDir :
	if os.path.exists(dest+i) == 0:
		os.mkdir(dest+i)

# loading names of channels folders inside language folders from source
listSubDir = []
for i in listDir :
	p = source+i
	listSubDir.append(os.listdir(p))

# creating names of channels folders inside language folders of destination
for i,j in zip(listDir,listSubDir) :
	for k in j:
		p = dest+i+'/'+k
		if os.path.exists(p) == 0:
			os.mkdir(p)

# Extraction of mfcc features and saving '.png' files inside respective channel folders of destination in grayscale format
for i in listDir :
	p1 = source+i
	p2 = dest+i
	for j in os.listdir(p1):
		q1 = p1+'/'+j
		q2 = p2+'/'+j+'/'
		for k in  os.listdir(q1):
			name = k.split('.')[0]+'.png'
			print(name)
			o1 = q1+'/'+k
			x, fs = librosa.load(o1)
			mfcc = librosa.feature.mfcc(x, sr=fs)
			librosa.display.specshow(mfcc, sr=fs, x_axis='time')
			plt.gray()
			plt.savefig(q2+name)

