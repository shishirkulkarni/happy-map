import numpy as np
import sys

#read tsv file


polarities = []
for x in sys.argv[1:]:
    print(x)
    with open(x, 'r', encoding="utf") as tsv_file:
        tsv = [line.strip().split('\t') for line in tsv_file]
    print("length of", x, ":", len(tsv))
    for row in tsv:
        if row[-1] == "NaN":  # exclude tweet without polarity
            continue
        polarities.append(np.double(row[-1]))

print("length of all: ", len(polarities))
polarities_np = np.array(polarities)
print("min polarities value:", polarities_np.min())
print("max polarities value:", polarities_np.max())
#with open(sys.argv[1], 'r', encoding="utf8") as tsv_file:
#	tsv = [line.strip().split('\t') for line in tsv_file]

#print(tsv)
