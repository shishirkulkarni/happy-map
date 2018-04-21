import csv
import sys

with open(sys.argv[1], 'r') as tsv_file:
	tsv = [line.strip().split('\t') for line in tsv_file]

sum = 0.0
count = 0
for row in tsv:
#	print row[-1]
#	sum += float(row[-1])
#	print sum
	count+=1

print count

#print sum/count

