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

dataDirectory = './data/cleaned/'

myColumn = 'Global Horizontal Radiation {Wh/m2}'

#vertical = 90
facadeAngle = 90

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

	print('*** FINISHED *** ')


'''
if tScale is a float or int it just scales the time by minutes
if tScale is a string options are:
	rt = real time running
	minute = hours converted to minutes
'''
def runAll(tScale):

	if tScale.isnumeric() or checkFloat(tScale):
		print('t scale is float or int')
	elif type(tScale) == str:
		print('t scale is str')

	print("tScale: " + str(tScale))

	allData = importData()
	singleColumn = getColumn(allData,myColumn)

	print(getColumn(allData,myColumn).iloc[3:10])
	print(surfaceOrientationConversion(singleColumn).iloc[3:10])

if __name__ == '__main__':
	runAll(2)