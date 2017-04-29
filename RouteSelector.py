import csv
import itertools
import re
import sys

MRTFULLCOMBI = []
SUTDLOOKUPTABLE = {}
MRTLOOKUPTABLE = []
START = 0
END = 37062
with open('MRTCombinations.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	MRTFULLCOMBI.append(row)

MRTCOMBI = MRTFULLCOMBI[START:END]

with open('Mrt to SUTD compiled.csv', 'rb') as f:
    reader = csv.reader(f)
    skip = True
    for row in reader:
    	if skip :
    		skip = False
    		continue
    	SUTDLOOKUPTABLE[row[0]] = int(row[3].strip(" min"))

with open('carTimeCompiled25clean.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	MRTLOOKUPTABLE.append(row)

# SUTDLOOKUP = open("Mrt to SUTD compiled.csv", "rb")		# This is a record of the travel time to drive from a given mrt to school
# SUTDLOOKUPREADER = csv.reader(SUTDLOOKUP)
# MRTLOOKUP = open("carTimeCompiled25clean.csv", "rb")	# This is the travel time to drive between stations
# MRTLOOKUPREADER = csv.reader(MRTLOOKUP)
MRTINDEX = {}
CACHE = {}

with open('mrtnames.csv', 'rb') as f:
    reader = csv.reader(f)
    counter = 0
    for row in reader:
    	name = row[0]
    	name = re.sub(", MRT"," MRT Station",name)
        MRTINDEX[name] = counter
        CACHE[name] = {}
        counter += 1

INVALID = ["N.A","Sorry"]
MAXTRAVELTIME = 60 # 1 hour

def lookup(origin, destination):
	if destination not in CACHE[origin]:
		originIndex = MRTINDEX[origin]
		destIndex = MRTINDEX[destination]
		if originIndex < destIndex:
			smaller = originIndex
			larger = destIndex
		else:
			smaller = destIndex
			larger = originIndex
		if MRTLOOKUPTABLE[smaller+1][larger] not in INVALID:
			# print MRTLOOKUPTABLE[smaller+1][larger+1]
			CACHE[origin][destination] = int(MRTLOOKUPTABLE[smaller+1][larger])
			return int(MRTLOOKUPTABLE[smaller+1][larger])
		print "Error!"
		print  origin + " to " + destination
		print str(originIndex)+":"+str(destIndex)
	else:
		# print CACHE[origin][destination]
		return CACHE[origin][destination]

def mrtToSchool(origin):
	return SUTDLOOKUPTABLE[origin] 

BEST_COMBI_RECORD = open("InitialOptimisedRoutes%sTo%s.csv"%(START,END),"w")

print "Starting ..."

for combi in MRTCOMBI:
	time = 1
	bestCombi = ()	
	prevBestTime = sys.maxint
	# print combi
	for subset in itertools.permutations(combi):
		for i in range(len(subset)-1):
			time += lookup(subset[i].strip("'").strip(" '"),subset[i+1].strip("'").strip(" '"))
		time += mrtToSchool(subset[len(subset)-1].strip("'").strip(" '"))	# find time to travel from last station to school
		# Implement algorithm to look up travel times to different locations -- lookup(origin,destination)
		if time < prevBestTime:
			prevBestTime = time
			bestCombi = subset
		time = 1
	if prevBestTime < MAXTRAVELTIME:
		print "best combi is " + str(bestCombi)
		print prevBestTime	
		BEST_COMBI_RECORD.write(str(bestCombi).strip("(").strip(")")+","+ str(prevBestTime) + "\n")

BEST_COMBI_RECORD.close()

print "END"