# import httplib
# conn = httplib.HTTPSConnection("http://www.streetdirectory.com/api/?mode=journey&output=xml&country=sg&q=103.82915135175699,1.307363769270172%20to%20103.84643694497719,1.2990493119206423&methods=driving&info=1&date=06/20/2011&time=02:38%20PM",80)
# conn.request("GET","/")
# r1 = conn.getresponse()
# print r1.status, r1.reason
# print r1.msg

# import urllib2
# response = urllib2.urlopen('http://www.streetdirectory.com/api/?mode=journey&output=xml&country=sg&q=103.8009211,1.4405828%20to%20103.84643694497719,1.2990493119206423&methods=driving&info=1&date=06/20/2011&time=02:38%20PM')
# html = response.read()
# print html



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import json
import time
import csv


MRT_STATIONS = []
with open('mrtnames.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	name = row[0]
    	name = re.sub(", MRT"," MRT Station",name)
        MRT_STATIONS.append(name);


# MRT_STATIONS = ["Tanah Merah MRT Station (EW4)" , "Expo MRT Station (CG1)" , "Bedok MRT Station (EW5)"]
URL = "http://www.streetdirectory.com/travel/"
LEAVE_TIME = "8:00 AM"
LEAVE_DATE = "17/04/2017"

driver = webdriver.Firefox()

class Car():

	def __init__(self,travel_time,travel_dist):
		self.travelTime = travel_time
		self.travelDist = travel_dist

	def getTravelTime(self):
		return self.travelTime

	def getTravelDist(self):
		return self.travelDist

	def info(self):
		return "Travel time is %s , travel distance is % s " %(self.travelTime, self.travelDist)

class Taxi():

	def __init__(self,travel_time,travel_fare):
		self.travelTime = travel_time
		self.travelFare = travel_fare

	def getTravelTime(self):
		return self.travelTime

	def getTravelFare(self):
		return self.travelFare

	def info(self):
		return "Travel time is %s , travel fare is % s " %(self.travelTime, self.travelFare)

class Bus():

	def __init__(self,travel_time,travel_fare):
		self.travelTime = travel_time
		self.travelFare = travel_fare

	def getTravelTime(self):
		return self.travelTime

	def getTravelFare(self):
		return self.travelFare

	def info(self):
		return "Travel time is %s , travel fare is % s " %(self.travelTime, self.travelFare)

class BusMrt():

	def __init__(self,travel_time,travel_fare):
		self.travelTime = travel_time
		self.travelFare = travel_fare

	def getTravelTime(self):
		return self.travelTime

	def getTravelFare(self):
		return self.travelFare

	def info(self):
		return "Travel time is %s , travel fare is % s " %(self.travelTime, self.travelFare)

def inputError(carTime,carDist,taxiTime,taxiFare,busFare,busTime,busMRTTime,busMRTFare,j):
	carTime.append("Error")
	carDist.append("Error")
	taxiTime.append("Error")
	taxiFare.append("Error")
	busFare.append("Error")
	busTime.append("Error")
	busMRTFare.append("Error")
	busMRTTime.append("Error")

MRT_MAPPING = {}
ERROR_LOG = open('ErrorLog.txt','w') 

carTimeCSV = open('carTime.csv','a')
carDistCSV = open('carDist.csv','a')
taxiTimeCSV = open('taxiTime.csv','a')
taxiFareCSV = open('taxiFare.csv','a')
busTimeCSV = open('busTime.csv','a')
busFareCSV = open('busFare.csv','a')
busMRTTimeCSV = open('busMRTTime.csv','a')
busMRTFareCSV = open('busMRTFare.csv','a')

carTimeCSV.write(','.join(MRT_STATIONS) + "\n")
carDistCSV.write(','.join(MRT_STATIONS) + "\n")
taxiTimeCSV.write(','.join(MRT_STATIONS) + "\n")
taxiFareCSV.write(','.join(MRT_STATIONS) + "\n")
busTimeCSV.write(','.join(MRT_STATIONS) + "\n")
busFareCSV.write(','.join(MRT_STATIONS) + "\n")
busMRTTimeCSV.write(','.join(MRT_STATIONS) + "\n")
busMRTFareCSV.write(','.join(MRT_STATIONS) + "\n")

startTime = time.time()
carTime = []
carDist = []
taxiTime = []
taxiFare = []
busTime = []
busFare = []
busMRTTime = []
busMRTFare = []
start = 
end = len(MRT_STATIONS)

for k in xrange(0,start):
	carTime.append("\n")
	carDist.append("\n")
	taxiTime.append("\n")
	taxiFare.append("\n")
	busFare.append("\n")
	busTime.append("\n")
	busMRTFare.append("\n")
	busMRTTime.append("\n")

for i in xrange(start,end):#len(MRT_STATIONS)):	# Change range here for different computers
	try:
		print "Checking for locations from " + MRT_STATIONS[i]
		MRT_MAPPING[MRT_STATIONS[i]] = {}
		driver.get(URL)
		try:
			close_advert = WebDriverWait(driver,10).until(EC.presence_of_element_located( (By.XPATH,"//*[@id=\"oss_layer1\"]/a") ) )
			close_advert.click()
		except TimeoutException:
			print "No advert found, continuing..."

		leaveTimeField = driver.find_element_by_id("time")
		# leaveTimeField.click()
		# leaveTimeField.clear()
		# leaveTimeField.send_keys(LEAVE_TIME)
		try:
			leaveBorder = driver.find_element_by_id("leaving-at").click()
			leaveTimeField.click()
			selectAM = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//*[@id=\"ptTimeSelectCntr\"]/div/div[2]/div[1]/div[2]/div[1]/div/div[1]/a[1]")))
			selectAM.click()
			selectTime = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//*[@id=\"ptTimeSelectCntr\"]/div/div[2]/div[1]/div[2]/div[1]/div/div[2]/a[8]")))
			selectTime.click();
			selectMin = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//*[@id=\"ptTimeSelectCntr\"]/div/div[2]/div[1]/div[2]/div[2]/div/div/a[1]")))
			selectMin.click();
		except TimeoutException:
			print "Did not find set time buttons!"
		try:
			setLeaveTimeField = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//*[@id=\"ptTimeSelectSetButton\"]/a")))
			setLeaveTimeField.click()
		except TimeoutException:
			print "Did not find set leave button!"

		leaveDateField = driver.find_element_by_id("date")
		leaveDateField.clear()
		leaveDateField.send_keys(LEAVE_DATE)
		try:
			dateButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id=\"ui-datepicker-div\"]/table/tbody/tr[4]/td[2]") ) )
			dateButton.click()
		except TimeoutException:
			print "date button could not be found!"

		try:
			applyButton = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/*[@id=\"leaving-at\"]/span[3]") ) )
			applyButton.click()
		except TimeoutException:
			print "Apply button could not be found!"
		#driver.find_element_by_xpath("/*[@id=\"leaving-at\"]/span[3]").click()	# Apply button

		driver.find_element_by_id("header_journey").click()
		try:
			from_location = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"travel_from") ) )
		except TimeoutException:
			print "Time out! Could not find field to enter location!"
			for j in xrange(i+1,len(MRT_STATIONS)):
				ERROR_LOG.write("Time out! Could not find field to enter location!\n")
				inputError(carTime,carDist,taxiTime,taxiFare,busFare,busTime,busMRTTime,busMRTFare,j)
			continue

		for k in xrange(0,i+1):
			carTime.append("N.A")
			carDist.append("N.A")
			taxiTime.append("N.A")
			taxiFare.append("N.A")
			busFare.append("N.A")
			busTime.append("N.A")
			busMRTFare.append("N.A")
			busMRTTime.append("N.A")

		print "Looping through all MRT Stations ..."
		for j in xrange(i+1,len(MRT_STATIONS)):
			try:
				
				to_location = driver.find_element_by_id("travel_to")
				
				from_location.send_keys(MRT_STATIONS[i])
				to_location.send_keys(MRT_STATIONS[j])
				driver.find_element_by_id("go_button").click()

				try:
					first_suggestion = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"infos\"]/table/tbody/tr[2]")))
					first_suggestion.click()
				except Exception , e:
					print "Did not find first suggestion for %s to %s " %(MRT_STATIONS[i], MRT_STATIONS[j])
					ERROR_LOG.write("Did not find first suggestion for %s to %s \n%s\n" %(MRT_STATIONS[i], MRT_STATIONS[j],e))
					inputError(carTime,carDist,taxiTime,taxiFare,busFare,busTime,busMRTTime,busMRTFare,j)


				try:
					second_suggestion = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"infos\"]/table/tbody/tr[2]")))
					second_suggestion.click()
				except Exception , e:
					print "Did not find second suggestion for %s to %s " %(MRT_STATIONS[i], MRT_STATIONS[j])
					ERROR_LOG.write("Did not find second suggestion for %s to %s \n%s\n" %(MRT_STATIONS[i], MRT_STATIONS[j],e))
					inputError(carTime,carDist,taxiTime,taxiFare,busFare,busTime,busMRTTime,busMRTFare,j)

				try:
					car_info_box = WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.ID, 'car-blk'), "min"))#EC.element_to_be_clickable((By.ID, 'car-blk'))) 
				except Exception , e:
					try:
						all_types = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"all_tab")))
						all_types.click()
					except Exception , e:
						print "Time out at %s stations to %s" %(MRT_STATIONS[i], MRT_STATIONS[j])
						ERROR_LOG.write("Time out at %s stations to %s\n%s\n" %(MRT_STATIONS[i], MRT_STATIONS[j],e))
						inputError(carTime,carDist,taxiTime,taxiFare,busFare,busTime,busMRTTime,busMRTFare,j)
						continue

				try:
					car_travel_time = driver.find_element_by_id("car_time").text
					car_travel_dist = driver.find_element_by_id("car_length").text
					taxi_travel_time = driver.find_element_by_id("taxi_time").text
					taxi_travel_fare = driver.find_element_by_id("taxi_fare").text
					bus_travel_time = driver.find_element_by_id("bus_time").text
					bus_travel_fare = driver.find_element_by_id("bus_fare").text
					bus_and_mrt_travel_time = driver.find_element_by_id("busmrt_time").text
					bus_and_mrt_travel_fare = driver.find_element_by_id("busmrt_fare").text

					carTime.append(car_travel_time)
					carDist.append(car_travel_dist)
					taxiTime.append(taxi_travel_time)
					taxiFare.append(taxi_travel_fare)
					busFare.append(bus_travel_fare)
					busTime.append(bus_travel_time)
					busMRTFare.append(bus_and_mrt_travel_fare)
					busMRTTime.append(bus_and_mrt_travel_time)

					MRT_MAPPING[MRT_STATIONS[i] ][MRT_STATIONS[j] ] = {"car": Car(car_travel_time , car_travel_dist),
																		"taxi": Taxi(taxi_travel_time , taxi_travel_fare),
																		"bus": Bus(bus_travel_time , bus_travel_fare),
																		"busmrt": BusMrt(bus_and_mrt_travel_time , bus_and_mrt_travel_fare) }
				except NoSuchElementException:
					print "Error at station %s to station %s "%(MRT_STATIONS[i],MRT_STATIONS[j])
					ERROR_LOG.write("Error at station %s to station %s , could not find element\n"%(MRT_STATIONS[i],MRT_STATIONS[j]))
					inputError(carTime,carDist,taxiTime,taxiFare,busFare,busTime,busMRTTime,busMRTFare,j)
			except TimeoutException , e:
				ERROR_LOG.write("Unhandled exception for station %s to station %s \nError : %s \n"%(MRT_STATIONS[i],MRT_STATIONS[j]),e)
				inputError(carTime,carDist,taxiTime,taxiFare,busFare,busTime,busMRTTime,busMRTFare,j)

		carTimeCSV.write(','.join(carTime)+"\n")
		carDistCSV.write(','.join(carDist)+"\n")
		taxiTimeCSV.write(','.join(taxiTime)+"\n")
		taxiFareCSV.write(','.join(taxiFare)+"\n")
		busTimeCSV.write(','.join(busTime)+"\n")
		busFareCSV.write(','.join(busFare)+"\n")
		busMRTTimeCSV.write(','.join(busMRTTime)+"\n")
		busMRTFareCSV.write(','.join(busMRTFare)+"\n")

		carTime = []
		carDist = []
		taxiTime = []
		taxiFare = []
		busTime = []
		busFare = []
		busMRTTime = []
		busMRTFare = []
	except TimeoutException , e:
		print "Unhandled Exception when searching from start location"
		ERROR_LOG.write("Unhandled Exception when searching from start location. \nError : %s \n" % e)
		for j in xrange(i+1,len(MRT_STATIONS)):
			ERROR_LOG.write("Time out! Could not find field to enter location!\n")
			inputError(carTime,carDist,taxiTime,taxiFare,busFare,busTime,busMRTTime,busMRTFare,j)
		continue


endTime = time.time()
elapsedTime = endTime - startTime

print "Elapsed time for %d stations, %d iterations is : %d" %(len(MRT_STATIONS), len(MRT_STATIONS)**2, elapsedTime)

# for i in MRT_MAPPING.keys():
# 	print "\nFrom " + i + " to :"
# 	for j in MRT_MAPPING[i].keys():
# 		print j + " via : "
# 		for k in MRT_MAPPING[i][j].keys():
# 			print k + " takes : " + MRT_MAPPING[i][j][k].info()

ERROR_LOG.close()
carTimeCSV.close()
carDistCSV.close()
taxiTimeCSV.close()
taxiFareCSV.close()
busTimeCSV.close()
busFareCSV.close()
busMRTTimeCSV.close()
busMRTFareCSV.close()

temp = json.dumps(MRT_MAPPING, default=lambda o: o.__dict__)
# print temp
# parsed = json.loads(temp)
# print json.dumps(parsed, indent=4, sort_keys=True)

with open('mrtTimings%d-%d.txt'%(start,end), 'w') as outfile:
    json.dump(temp, outfile)

# count = 0
# for i in xrange(1,165):
# 	count += i

# print count