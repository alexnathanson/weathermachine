import csv
import os
import pandas as pd
import logging
import time
from datetime import datetime
from arduinoSerial import ArduinoSerial as Arduino #this is the code for communicating with an Arduino via serial
from WeatherMachineLights import WMLights as Lights	
import math
import sys
import api
from threading import Thread
from queue import Queue
from _thread import interrupt_main
import requests
import json

dataDirectory = './data/cleaned/'

devMode = False

#arduino = object

#import date from the file specified via the browser
def importData(dataFileName):

	# dirList = os.listdir(dataDirectory)
	fileName = dataDirectory + dataFileName

	print("importing data from " + fileName)

	try:
		with open(fileName) as csvfile:
			df = pd.read_csv(fileName)
			print(df.head())
	except IOError:
		print('failed to import ' + fileName)
		logging.exception('')
		raise SystemExit(1)
	return df

def mergeTwoColumns(c1, c2):
	return pd.merge(c1,c2,left_index=True,right_index=True)

#check if this is a float or not
def checkFloat(toCheck):

	try:
		float(toCheck)
		return True
	except ValueError:
		return False

#run through all times at specified rate
def runLoop(dF):

	dataIndex = 0

	while True:
		print('run loop')
		#get time

		#if no more data exit loop
		if dataIndex == len(dF) - 1:
			break

		dataIndex = dataIndex + 1

	print('')
	print('*** FINISHED *** ')
	print('')

#prints a progress bar on the console
#note that the terminal window needs to be wide enough to fit all text otherwise it will look wierd
def progressBar(iteration, total, prefix = 'Progress', suffix = 'Complete', suffix2 = 'Min Remaining', decimals = 1, length = 100, fill = '█', printEnd = "\r"):

    #prefix = "Progress"
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	estMin = total - iteration
	print(f'\r{prefix} |{bar}| {iteration}% {suffix} {estMin} {suffix2}', end = printEnd)
	
	if iteration == 100:
		print()

'''
if tScale is a float or int it just scales the time by minutes
if tScale is a string options are:
	rt = real time running
	minute = hours converted to minutes
	seconds = hours converted to seconds
'''
def setTimeScale(tScale):
	if str(tScale).isnumeric() or checkFloat(tScale):
		print('t scale is float or int')
	elif type(tScale) == str:
		print('t scale is str')
		if tScale == 'rT':
			tScale = 1
		elif tScale == 'minute':
			tScale = 60
		elif tScale == 'seconds':
			tScale = 60 * 60
		else:
			tScale = 1

	print("new time scale: " + str(tScale))

	return tScale
	
def runLights(lData, azimuth):
	print("running lights")

	#print(lData.head())

	#instantiate the light class
	lights = Lights(azimuth)

	#print(cList)

	#create lights dataframe
	initData = {'Date':lData['Date'],'HH:MM': lData["HH:MM"]}#,lData.columns[0]:mCData
	dfLights = pd.DataFrame(initData)
	#print(dfLights.head())

	#convert the data to the proper surface
	#get the column of data we want
#	mCData = lData.iloc[:,2]
#	print(mCData.iloc[0:10])
#s	dfLights['surface conversion'] = lights.roughSurfaceOrientationConversion(mCData)

	dfLights['surface irradiance'] = lights.detailedSurfaceOrientation(lData)

	#convert from energy to lux
	dfLights['lux'] = lights.energyToLux(dfLights['surface irradiance'])

	#map lux to arduino analog range (0 to 255)
	dfLights['ard'] = lights.convertToArduinoAnalogOutput(dfLights['lux'], 120000)
	#print(dfLights.iloc[0:10])

	return dfLights

def apiThread(outQ):
	#start API
	api.app.run()	

def runMachine():
	global arduino

	print('')
	print("*** Running Weather Machine ***")
	
	# print("wall azimuth: " + str(azimuth) + " degrees")
	# print("time scale: " + str(tScale))
	print("Arduino port: " + api.runSettings['port'])
	dataFile = api.runSettings['file'] + ".csv"
	print("Data file: " + dataFile)
	print("Facade: " + api.runSettings['facade'])

	#convert cardinal direction to azimuths
	if api.runSettings['facade'] == 'north':
		az = 0
	elif api.runSettings['facade'] == 'east':
		az = 90
	elif api.runSettings['facade'] == 'south':
		az = 180
	elif api.runSettings['facade'] == 'west':
		az = 270

	print("Timescale: " + api.runSettings['time'])
	
	components=''
	if api.runSettings['light'] == 'true':
		components = components + "lights "

	if components == '':
		components = 'none'

	print("Components: " + components)
	print('')

	try:
		#global arduino
		arduino = Arduino(api.runSettings['port'])
	except Exception as e:
		print(e)
		#interrupt_main()
		raise SystemExit(1)

	#rate that data is sent - currently not being used
	#tScale = setTimeScale(tScale)

	#get all the data in a dataframe
	allData = importData(dataFile)

	###### LIGHTS ######
	if api.runSettings['light'] == 'true':
		# columns needed for light calculations:
		lightCols = ['Date', 'HH:MM', 'Global Horizontal Radiation {Wh/m2}','Direct Normal Radiation {Wh/m2}','Diffuse Horizontal Radiation {Wh/m2}']
		dfLights = runLights(allData[lightCols], az)
		print(dfLights.head())

	print("Output:")

	startTime = datetime.now()

	stats = {"percent":0,"elapsedTime":0,"estimatedRemainingTime":0,"light":0}



	dFLen = len(dfLights)

	#convert df to json for POSTing
	jsonLights = {}
	for i in range(dFLen):
		jsonLights[dfLights['Date'][i] + " " + dfLights['HH:MM'][i]] = int(dfLights['ard'][i])

	#print(jsonLights)
	postToAPI('data', json.dumps(jsonLights))

	for i in range(dFLen):
		if api.runIt == False:
			arduino.turnOff()
			arduino.serialObj.close()
			break
		elif api.runIt == True:

			lB = dfLights['ard'][i]
			#print("Sending: " + str(lB))
			arduino.sendByte(str(lB).encode())

			#run stats
			stats['percent'] = float((i+1) / dFLen)
			stats['elapsedTime'] = int((datetime.now() - startTime).total_seconds())
			stats['estimatedRemainingTime'] = (stats['elapsedTime'] / stats['percent']) * (100 - stats['percent'])
			#stats['light'] = int(lB)
			# if len(stats['light']) <= 0:
			# 	stats['light'] = [lB]
			# else:
			# 	#stats['light']=
			# 	stats['light'].append(lB)
			#print(str(round(stats['percent'],3)) + "% - " + str(stats['elapsedTime']) + " seconds - " + str(stats['estimatedRemainingTime']) + " seconds")

			# url = 'http://localhost:5000/runStats'
			# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
			# x = requests.post(url, data=json.dumps(stats), headers=headers)

			postToAPI('runStats', stats)

		 	#this is in seconds
			time.sleep(1)

	api.runIt = False

def postToAPI(endPoint,pData):
	url = 'http://localhost:5000/' + endPoint
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	x = requests.post(url, data=json.dumps(pData), headers=headers)

def runAll():

	#Object that signals shutdown
	_sentinel = object()

	q = Queue()
	t1 = Thread(target = apiThread, args =(q, ), daemon = True)
	t1.start()

	try:
		while True:
			if api.runIt == True:
				runMachine()
			time.sleep(3)
	except KeyboardInterrupt:
		#t1.join()
		print("Keyboard Interrupt Exception")

		#turn off the arduino outputs if possible
		try:
			arduino.turnOff()
		except:
			pass
		#raise SystemExit(1)

if __name__ == '__main__':
	runAll()