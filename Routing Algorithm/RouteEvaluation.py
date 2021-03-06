import csv
import RouteSelector	# To obtain MAXTRAVELTIME per route
import PossibleCombinationsForBuses	# To obtain the number of routes planned out - NUMBUSES
import pathFinderUpdated	# To obtain the maximum capacity per route

ITER = 4

def run():
	print "Start"

	possibleRoutes = []
	FileToOptimise = "SortedOptimisedRoutes%s.csv"%ITER # "PossibleRoutesToConsider.csv"
	if FileToOptimise == "SortedOptimisedRoutes%s.csv"%ITER:
		NUMBUSES = 1
	else:
		NUMBUSES = PossibleCombinationsForBuses.NUMBUSES

	with open( FileToOptimise , "rb") as f:
		reader = csv.reader(f)
		for row in reader:
			possibleRoutes.append(row)

	print "Finished reading in data"

	MAXTOTALTIME = (RouteSelector.MAXTRAVELTIME * NUMBUSES)
	MAXTOTALPAX = pathFinderUpdated.MAXCAP * NUMBUSES

	print "Begininning scoring ..."
	for i in possibleRoutes:
		timeScore = (MAXTOTALTIME - float(i[0]) ) / MAXTOTALTIME
		paxScore = float(i[1]) / MAXTOTALPAX
		totalScore = timeScore + paxScore		# This gives equal weightage to both travel time and num of ppl served. They are both normalised to their own values. A value closest to 2 is the best result
		i.insert(0,totalScore)

	possibleRoutes.sort(key=lambda x : x[0])	# sort by the score allocated to each route

	print "Saving out results ..."

	with open("RoutesAfterScoring%s.csv"%ITER,"wb") as f:
		writer = csv.writer(f)
		writer.writerow(["Score","Route Travel Time","Number of pax served","Route"])
		for i in possibleRoutes:
			writer.writerow(i)

	print "END"

if __name__ == "__main__":
	run()