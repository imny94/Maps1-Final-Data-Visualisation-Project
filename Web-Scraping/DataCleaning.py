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

URL = "http://www.streetdirectory.com/travel/"
LEAVE_TIME = "8:00 AM"
LEAVE_DATE = "17/04/2017"

driver = webdriver.Firefox()
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

def checkForInfoFrom(origin,destination):
	to_location = driver.find_element_by_id("travel_to")
				
	from_location.send_keys(origin)
	to_location.send_keys(destination)
	driver.find_element_by_id("go_button").click()

	try:
		first_suggestion = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"infos\"]/table/tbody/tr[2]")))
		first_suggestion.click()
	except (TimeoutException , ElementNotVisibleException ) , e:
		print "Did not find first suggestion for %s to %s " %(MRT_STATIONS[i], MRT_STATIONS[j])

	try:
		second_suggestion = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"infos\"]/table/tbody/tr[2]")))
		second_suggestion.click()
	except (TimeoutException , ElementNotVisibleException ) , e:
		print "Did not find second suggestion for %s to %s " %(MRT_STATIONS[i], MRT_STATIONS[j])

	try:
		car_info_box = WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.ID, 'car-blk'), "min"))#EC.element_to_be_clickable((By.ID, 'car-blk'))) 
	except Exception , e:
		try:
			all_types = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"all_tab")))
			all_types.click()
		except Exception , e:
			print "Time out at %s stations to %s" %(MRT_STATIONS[i], MRT_STATIONS[j])
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

filesToCheck = []

newCSVRows = []
listOfChanges = {} # {"MRT" : [carTime,carDist,taxiTime, taxiFare, busFare , busTime, busMRTFare, busMRTTime ]}

for i in filesToCheck:
	with open(i,'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			newRow = row
			for j in newRow:
				if j == "Error":
					pass
				elif j == "Sorry":
					pass
				elif j == "Not Available":
					pass
