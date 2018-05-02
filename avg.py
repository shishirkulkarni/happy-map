import sys
import os
import numpy as np

def list_files(dir):
	r = []
	subdirs = [x[0] for x in os.walk(dir)]
	for subdir in subdirs:
		files = os.walk(subdir).__next__()[2]
		if(len(files) > 0):
			for file in files:
				if file == 'part-00000':
					r.append(subdir + "\\" + file)
	return r

def write_polarity(file):
	#read tsv file
	with open(file, 'r', encoding="utf8") as tsv_file:
		tsv = [line.strip().split('\t') for line in tsv_file]

	#average polarity for all tweets in file
	sum = np.double(0)
	count = np.int(0)
	for row in tsv:
		if row[-1] == "NaN": #exclude tweet without polarity
			continue
		sum += np.double(row[-1])
		#print(count, row[-1], sum)
		count+=1

	##### write file with <key,val> = <locn, polarity>####
	subdirs = file.split('\\')
	headers = subdirs[-2].split('_')
	if 'OUT' in headers:
		headers.remove('OUT')
	if 'output' in headers:
		headers.remove('output')
	key = headers[0]
	value = str(sum/count)

	#write polarity to each subdir
	newpath = '\\'.join(subdirs[0:len(subdirs)-1]) + '\\polarity.tsv'
	f = open(newpath, 'w+')
	f.write(key + '\t' + value)
	f.close()
		#print(key + '\t' + value)

def main():
	files = list_files('data')

	for file in files:
		write_polarity(file)

if __name__ == "__main__": main()