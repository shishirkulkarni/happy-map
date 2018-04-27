import sys
import numpy as np
from numpy import linalg as LA
from sklearn import preprocessing
import re

#read tsv file
with open(sys.argv[1], 'r', encoding="utf8") as tsv_file:
	tsv = [line.strip().split('\t') for line in tsv_file]

#average polarity for all tweets in file
topic = sys.argv[1].split('\\')[2]

polarities = []
for row in tsv:
	if row[-1] == "NaN": #exclude tweet without polarity
		continue
	polarities.append(np.double(row[-1]))

min_val = np.double(-0.5423)
max_val = np.double(0.5719)
polarities_np = np.array(polarities)

polarities_norm = 10*((polarities_np - min_val)/(max_val - min_val)) # normalize from 0 to 10

print(topic + "\t" + str(polarities_norm.mean()))
