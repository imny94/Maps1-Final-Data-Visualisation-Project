import csv
import re

ITER = 4

def run():
	unsorted = []

	formatList = []
	print "Starting ..."
	with open("InitialOptimisedRoutes%s.csv"%ITER,"rb") as f:
		reader = csv.reader(f)
		for row in reader:
			for i in row:
				tempName = i
				tempName = re.sub(r'([^\s\w]|_)+', '', tempName)
				formatList.append(tempName)
			unsorted.append(formatList)
			formatList = []
	print "Done reading in Initial optimised routes ... "
	MRT_STATIONS = {}				# This is to record the number of people served per station
	with open('mrtnamesTest%s.csv'%ITER, 'rb') as f:
	    reader = csv.reader(f)
	    skip = True
	    for row in reader:
	    	if skip:
	    		skip = False
	    		continue
	    	name = row[0]
	    	name = re.sub(", MRT"," MRT Station",name)
	        MRT_STATIONS[name] = int(row[1])

	temp = {}
	for i in unsorted:	# To initialise the dictionary
		temp[i[-1] ] = []

	# print unsorted[1]
	for i in unsorted:
		temp[i[-1] ].append(i[:len(i)-1])	# To add the various combinations to the timing

	sortedList = []
	# print temp
	print "Sorting now ..."
	for i in sorted(temp.keys()):	# Use the sorted keys
		for j in temp[i]:			# And access each of the combinations allocated to each time
			tempList = [i]			# Add back time for each route back into the different rows
			numPax = 0
			for k in j:
				# print k
				tempList.append(k)
				numPax += MRT_STATIONS[k.strip("' ").strip("'")]
			tempList.insert(1, numPax)	# Stores the number of people served as the second column in file
			sortedList.append(tempList)

	print "Saving out results ..."
	with open("SortedOptimisedRoutes%s.csv"%ITER,"wb") as f:
		writer = csv.writer(f)
		for i in sortedList:
			writer.writerow(i)

	print "END"

if __name__ == "__main__":
	run()