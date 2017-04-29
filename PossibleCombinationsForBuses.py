import itertools
import csv

initialRoutes = []
possibleRoutes = []
NUMBUSES = 5

with open("SortedOptimisedRoutes.csv","rb") as f:
	reader = csv.reader(f)
	for row in reader:
		initialRoutes.append(row)


for subSet in itertools.combinations(initialRoutes,NUMBUSES):	# Subset is the list of all possible combinations
	for i in subSet:	# For each possible combination
		temp = {}
		for j in i:		# Get the various routes in each combination
			norepeat = True
			if norepeat:
				for k in xrange(2,len(j)):	# loop through locations in each route
					if k not in temp:
						temp[k] = 0
					else:					# Indicates that this route has overlaps
						norepeat = false
						break				# So can stop checking this combination
			else:
				break


			possibleRoutes.append(i)	# Record this route as a feasible route

for i in possibleRoutes:		# This is to record the time taken and the number of people served per route
	time = 0
	pplServed = 0
	for j in i:
		time += j[0]
		pplServed += j[1]
	possibleRoutes[i].insert(0,time)
	possibleRoutes[i].insert(1,pplServed)

with open("PossibleRoutesToConsider.csv","w") as f:
	writer = csv.writer(f)
	for row in possibleRoutes:
		writer.writerrow(row)