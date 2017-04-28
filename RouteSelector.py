import csv
import itertools

MRTCOMBI = {}

with open('MRTCombinations.csv', 'rb') as f:
    reader = csv.reader(f)
    skip = True
    for row in reader:
    	MRTCOMBI[row[0,len(row)-2]] = row[-1]

# SUTDLOOKUP = open("MRTTOSUTD.csv", "rb")
# SUTDLOOKUPREADER = csv.reader(SUTDLOOKUP)
# MRTLOOKUP = open("MRTTOMRT.csv", "rb")
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
	originIndex = MRTINDEX[origin]
	destIndex = MRTINDEX[destination]
	if destination not in CACHE[origin]:
		if MRTLOOKUPREADER[originIndex+1][destIndex] not in INVALID: # +1 for origin index as file has mrt station names for first row
			# good to go
			return MRTLOOKUPREADER[originIndex+1][destIndex]
		else:
			# Take time from destination index
			if MRTLOOKUPREADER[destIndex][originIndex+1] not in INVALID:
				return MRTLOOKUPREADER[destIndex][originIndex+1]
			else:
				print "ERROR"
	else:
		return CACHE[origin][destination]

def mrtToSchool(origin):
	originIndex = MRTINDEX[origin]
	return SUTDLOOKUPREADER[1][originIndex] # First row of file is station name, second row is timing

BEST_COMBI_RECORD = open("InitialOptimisedRoutes.csv","w")

for L in range(0, len(MRTCOMBI)):
	time = 0
	prevBestTime = sys.maxint
	bestCombi = ()
    for subset in itertools.permutations(MRTCOMBI.keys(), L):
    	for i in xrange(len(subset)):
    		time += lookup(subset[i],subset[i+1])
		time += mrtToSchool(subset[len(subset)-1])	# find time to travel from last station to school
    	# Implement algorithm to look up travel times to different locations -- lookup(origin,destination)
		if time < prevBestTime:
			prevBestTime = time
			bestCombi = subset
		if prevBestTime < MAXTRAVELTIME:
			BEST_COMBI_RECORD.write(str(bestCombi).strip("(").strip(")")+","
										+ str(prevBestTime) + "\n")

BEST_COMBI_RECORD.close()

