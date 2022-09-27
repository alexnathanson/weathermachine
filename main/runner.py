'''
clean data is defined here as data with 1 single row of headers.
it does not necessarily mean there aren't problems in the data

HEADERS:
Date
HH:MM
Datasource
Dry Bulb Temperature {C}
Dew Point Temperature {C}
Relative Humidity {%}
Atmospheric Pressure {Pa}
Extraterrestrial Horizontal Radiation {Wh/m2}
Extraterrestrial Direct Normal Radiation {Wh/m2}
Horizontal Infrared Radiation Intensity from Sky {Wh/m2}
Global Horizontal Radiation {Wh/m2}
Direct Normal Radiation {Wh/m2}
Diffuse Horizontal Radiation {Wh/m2}
Global Horizontal Illuminance {lux}
Direct Normal Illuminance {lux}
Diffuse Horizontal Illuminance {lux}
Zenith Luminance {Cd/m2}
Wind Direction {deg}
Wind Speed {m/s}
Total Sky Cover {.1}
Opaque Sky Cover {.1}
Visibility {km}
Ceiling Height {m}
Present Weather Observation
Present Weather Codes
Precipitable Water {mm}
Aerosol Optical Depth {.001}
Snow Depth {cm}
Days Since Last Snow
Albedo {.01}
Liquid Precipitation Depth {mm}
Liquid Precipitation Quantity {hr}
'''

import csv
import os
import pandas as pd
import logging
import time
import arduinoSerial #this is the code for communicating with an Arduino via serial
from WeatherMachineLights import WMLights as Lights	


dataDirectory = './data/cleaned/'

myColumn = 'Global Horizontal Radiation {Wh/m2}'

#cardinal direction in degrees - east = 90, south = 180, west = 270, north = 0
azimuth = 180

def importData():

	dirList = os.listdir(dataDirectory)
	fileName = dataDirectory + dirList[0]

	print("importing data from " + fileName)

	try:
		with open(fileName) as csvfile:
			df = pd.read_csv(fileName)
			print(df.head())
	except IOError:
		print('failed to import ' + fileName)
		logging.exception('')
	
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
def printProgressBar(iteration, total, prefix = 'Progress', suffix = 'Complete', suffix2 = 'Min Remaining', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	"""
	src: https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters

    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """

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

def runAll(tScale):

	print('')
	print("*** Running Weather Machine ***")
	print("modules: Lights")
	print("wall azimuth: " + str(azimuth) + " degrees")
	print("time scale: " + str(tScale))
	print('')

	#instantiate the light class
	lights = Lights(azimuth)

	tScale = setTimeScale(tScale)

	#get all the data in a dataframe
	allData = importData()

	#get the column of data we want
	mCData = allData[myColumn]
	#convert the data to the proper surface
	mCDataToSurface = lights.surfaceOrientationConversion(mCData)
	#convert from energy to lux
	mCDataToLux = lights.energyToLux(mCData)

	#merge our converted data + with time stamp column into 1 dataframe
	outputColumns = mergeTwoColumns(mCDataToLux,allData["HH:MM"])
	print("Output:")
	print(outputColumns.iloc[3:10])

	# WILL THE DATA ALWAYS BE IN THIS FORMAT i.e. 1 row per hour?
	print(outputColumns['HH:MM'].head())
	print(len(outputColumns))


	dFLen = len(outputColumns)
	for i in range(dFLen):
		#if you print anything after the progress bar it will get messed up
		printProgressBar(round((i+1)/dFLen,2),dFLen) 
		#run next data

		#this is in seconds
		time.sleep(1)

if __name__ == '__main__':
	runAll(2)