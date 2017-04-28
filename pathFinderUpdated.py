import copy
import csv
import re

# MRT_STATIONS = []
MRT_STATIONS = {}
with open('mrtnamesTest.csv', 'rb') as f:
    reader = csv.reader(f)
    skip = True
    for row in reader:
    	if skip:
    		skip = False
    		continue
    	# name = row[1]
    	name = row[0]
    	name = re.sub(", MRT"," MRT Station",name)
        # MRT_STATIONS.append(name)
        # MRT_STATIONS[name] = row[5]
        MRT_STATIONS[name] = row[1]

MAXVISITS = 5
MAXCAP = 50 # Allow some over-crowding
MINPAX = 35

listOfConfigurations = []
MRTPermutations = open('MRTCombinations.csv','w')

print "starting..."

import itertools
for i in xrange(0,MAXVISITS+1):
	for subSet in itertools.combinations(MRT_STATIONS.keys(),i):
		counter = 0
		write = True
		for j in subSet:
			counter += int(MRT_STATIONS[j])
			if counter > MAXCAP:
				write = False
				break
		if counter < MINPAX:
			write = False	
		if write:
			# print str(subSet) +" : " +  str(counter)
			MRTPermutations.write(str(subSet).strip("(").strip(")")+","+str(counter)+"\n")


# for i in xrange(0,MAXVISITS+1):
# 	for subSet in itertools.permutations(MRT_STATIONS.keys(),i):
# 		counter = 0
# 		write = True
# 		for j in subSet:
# 			counter += int(MRT_STATIONS[j])
# 			if counter > MAXCAP:
# 				write = False
# 				break
# 		if write:
# 			MRTPermutations.write(str(subSet).strip("(").strip(")")+"\n")


MRTPermutations.close()

