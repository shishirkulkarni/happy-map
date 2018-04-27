import sys
import numpy as np

#read tsv file
with open(sys.argv[1], 'r', encoding="utf8") as tsv_file:
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

print("polarity =", str(sum/count))

