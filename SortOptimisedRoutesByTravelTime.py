import csv

unsorted = []


with open("InitialOptimisedRoutes.csv","rb") as f:
	reader = csv.reader(f)
	for row in reader:
		unsorted.append(row)

MRT_STATIONS = {}				# This is to record the number of people served per station
with open('mrtnamesTest.csv', 'rb') as f:
    reader = csv.reader(f)
    skip = True
    for row in reader:
    	if skip:
    		skip = False
    		continue
    	name = row[0]
    	name = re.sub(", MRT"," MRT Station",name)
        MRT_STATIONS[name] = row[1]

temp = {}
for i in unsorted:	# To initialise the dictionary
	temp[i[-1] ] = []

for i in unsorted:
	temp[i[-1] ].append(i[:len(i)-1])	# To add the various combinations to the timing

sortedList = []

for i in sorted(temp.keys()):	# Use the sorted keys
	for j in temp[i]:			# And access each of the combinations allocated to each time
		tempList = [i]			# Add back time for each route back into the different rows
		numPax = 0
		for k in j:
			tempList.append(k)
			numPax += MRT_STATIONS[k]
		tempList.insert(1, numPax)	# Stores the number of people served as the second column in file
		sortedList.append(tempList)

with open("SortedOptimisedRoutes.csv","w") as f:
	writer = csv.writer(f)
	for i in sortedList:
		writer.writerow(i)