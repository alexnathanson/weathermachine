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
import serial #for serial communication with  Arduino via USB
import time #just for testing purposes, can be removed later

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

def getColumn(dF, mC):
	return dF[mC]

#convert Wh/m2 to Lux
def energyToLux():
	print("energy to lux converion")

'''
convert from horizontal point to a particular vertical face

rough conversion of light intensity for different azimuths
east (90) = 75%
south (180) = 100%
west (270) = 75%
north (0) = 10%
'''
def surfaceOrientationConversion(dFC):
	print("surface conversion")

	#azimuth conversation
	if azimuth == 0: #north
		azScaler = .1
	elif azimuth == 90: #east
		azScaler = .75
	elif azimuth == 180: #south
		azScaler = 1.0
	elif azimuth == 270: #west
		azScaler = .75

	convertedColumn = dFC * azScaler

	return convertedColumn

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

def printProgressBar(iteration, total =100, prefix = 'Progress', suffix = 'Complete', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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
	print(f'\r{prefix} |{bar}| {iteration}% {suffix}', end = printEnd)
	
	if iteration == 100:
		print()

'''
if tScale is a float or int it just scales the time by minutes
if tScale is a string options are:
	rt = real time running
	minute = hours converted to minutes
'''
def runAll(tScale):

	print('')
	print("*** Running Weather Machine ***")
	print("modules: Lights")
	print("wall azimuth: " + str(azimuth) + " degrees")
	print("time scale: " + str(tScale))
	print('')

	if str(tScale).isnumeric() or checkFloat(tScale):
		print('t scale is float or int')
	elif type(tScale) == str:
		print('t scale is str')

	allData = importData()
	singleColumn = getColumn(allData,myColumn)

	print(getColumn(allData,myColumn).iloc[3:10])
	print(surfaceOrientationConversion(singleColumn).iloc[3:10])

	#for testing
	for i in range(100):
		printProgressBar(i+1) 
		time.sleep(1)

if __name__ == '__main__':
	runAll(2)