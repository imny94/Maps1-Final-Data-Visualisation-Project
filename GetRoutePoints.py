import urllib2
import json
import csv
# http://www.streetdirectory.com/api/?mode=journey&output=xml&country=sg&q=103.80076209350,1.4406374767246%20to%20103.849425,1.370194&methods=driving&info=1&date=06/20/2011&time=02:38%20PM
originCoord = str()	# 103.80076209350,1.4406374767246
destCoord = str()	# 103.849425,1.370194
date = str()		# 06/20/2011
time= str()			# 02:38
AMorPM = str()		# PM or AM
response = urllib2.urlopen('http://www.streetdirectory.com/api/?mode=journey&output=json&country=sg&q=103.80076209350,1.4406374767246%20to%20103.849425,1.370194&methods=driving&info=1&date=06/20/2011&time=02:38%20PM')#'http://www.streetdirectory.com/api/?mode=journey&output=xml&country=sg&q=' + originCoord + '%20to%20'+ destCoord + '&methods=driving&info=1&date='+ date + '&time=' + time + '%20' + AMorPM)
html = response.read()

htmlData = json.loads(html)

with open("SampleRoute.csv","wb") as f:

	for i in htmlData['routes']:
		f.write(i['x'] + "," + i['y'] + '\n')
