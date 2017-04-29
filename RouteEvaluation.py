import csv
import RouteSelector	# To obtain MAXTRAVELTIME per route
import PossibleCombinationsForBuses	# To obtain the number of routes planned out - NUMBUSES
import pathFinderUpdated	# To obtain the maximum capacity per route

print "Start"

possibleRoutes = []
with open("PossibleRoutesToConsider.csv","rb") as f:
	reader = csv.reader(f)
	for row in reader:
		possibleRoutes.append(row)

print "Finished reading in data"

MAXTOTALTIME = (RouteSelector.MAXTRAVELTIME * PossibleCombinationsForBuses.NUMBUSES)
MAXTOTALPAX = pathFinderUpdated.MAXCAP * PossibleCombinationsForBuses.NUMBUSES

print "Begininning scoring ..."
for i in possibleRoutes:
	timeScore = (MAXTOTALTIME - i[0]) / MAXTOTALTIME
	paxScore = i[1] / MAXTOTALPAX
	totalScore = timeScore + paxScore		# This gives equal weightage to both travel time and num of ppl served. They are both normalised to their own values. A value closest to 2 is the best result
	i.insert(0,totalScore)

possibleRoutes.sort(key=lambda x : x[0])	# sort by the score allocated to each route

print "Saving out results ..."

with open("RoutesAfterScoring.csv","rb") as f:
	writer = csv.writer(f)
	for i in possibleRoutes:
		writer.wrterow(i)

print "END"