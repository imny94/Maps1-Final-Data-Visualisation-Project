import copy

MRT_STATIONS = ["a","b","c","d","e"]
MAXVISITS = 3

listOfConfigurations = []

# This works!! 
def visit(hayStack, currentSize, currentConfig):
	print "haystack is : "  
	print hayStack
	print "\n"
	for i in hayStack:
		if currentSize < MAXVISITS - 1:
			if i in currentConfig:
				continue
			currentConfig.append(i)
			visit(hayStack[1:],currentSize+1,currentConfig) 
			currentConfig.pop()
		else:
			if i in currentConfig:
				continue
			currentConfig.append(i)
			
			print "\ncurrentConfig is : "
			print currentConfig
			listOfConfigurations.append(copy.deepcopy(currentConfig))
			currentConfig.pop()

# visit(MRT_STATIONS,0,[])
# print listOfConfigurations

def visitCombinations(haystack,currentConfig):
	for i in xrange(len(haystack)):
		counter = i
		for j in xrange(MAXVISITS-1):
			if counter > len(haystack) - 1:
				break
			currentConfig.append(haystack[counter])
			counter += 1
		for j in haystack[i+MAXVISITS-1:]:
			currentConfig.append(j)
			print currentConfig
			currentConfig.pop()
		currentConfig = []

# visitCombinations(MRT_STATIONS,[])
import itertools
for i in xrange(0,MAXVISITS+1):
	for subSet in itertools.combinations(MRT_STATIONS,i):
		print subSet