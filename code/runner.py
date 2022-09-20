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

#convert from horizontal point to a particular vertical face
def surfaceConversion():
	print("surface conversion")

#run through all times at specified rate
def runLoop():
	print('run loop')

def runAll(tScale):
	print("tScale: " + str(tScale))

	allData = importData()
	singleColumn = getColumn(allData,myColumn)


	print(getColumn(allData,myColumn).iloc[3:10])

if __name__ == '__main__':
	runAll(2)