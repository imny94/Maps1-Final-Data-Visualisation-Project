import itertools
import csv

initialRoutes = []
possibleRoutes = []
NUMBUSES = 2

def run():
	print "Starting..."
	with open("SortedOptimisedRoutes.csv","rb") as f:
		reader = csv.reader(f)
		for row in reader:
			initialRoutes.append(row)
	print "Finished reading in sorted routes"
	print "Starting combinational loop"
	for subSet in itertools.combinations(initialRoutes,NUMBUSES):	# Subset is the list of all possible combinations
		innerBreak = False
		for i in subSet:	# For each possible combination
			if innerBreak:
				break
			temp = set()
			norepeat = True
			# print i
			for j in i:		# Get the various routes in each combination
				if norepeat:
					for k in j:	# loop through locations in each route
						if k not in temp:
							temp.add(k)
						else:					# Indicates that this route has overlaps
							# print "Breaking inner ... "
							norepeat = False
							break				# So can stop checking this combination
				else:
					# print "Breaking out"
					innerBreak = True
					break
		if not innerBreak:
			print "Found a possible route!"
			print i
			possibleRoutes.append(i)	# Record this route as a feasible route
	print "Completed iterating to check for possible collection of routes"
	for i in possibleRoutes:		# This is to record the time taken and the number of people served per route
		time = 0
		pplServed = 0
		for j in i:
			time += j[0]
			pplServed += j[1]
		possibleRoutes[i].insert(0,time)
		possibleRoutes[i].insert(1,pplServed)
	print "Saving out results..."
	with open("PossibleRoutesToConsider.csv","w") as f:
		writer = csv.writer(f)
		for row in possibleRoutes:
			writer.writerrow(row)

	print "END"

if __name__ == "__main__":
	run()