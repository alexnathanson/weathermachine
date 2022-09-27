#this code is for the weather machine's lighting elements

import pandas as pd
import math

class WMLights:
	def __init__(self, azimuth):
		self.azimuth = azimuth

	'''
	convert Wh/m2 to Lux
	source: "A conversion guide: solar irradiance and lux illuminance", https://www.extrica.com/article/21667/pdf
	"The analysis and measurement show the irradiance to illuminance conversion factor is
	1 W/m2 equals 116 ± 3 lx for indoor LED based solar simulators and 122 ± 1 lx for outdoor natural sunlight.
	An engineering rule of thumb is 120 lx equals 1 W/m2, or 1 Sun equals 120000 lx."

	Note that a more accurate number could probably be used with a precise understanding of the LED light wavelengths
	'''
	def energyToLux(self, ser):
		print("energy to lux converion: 1W/m^2 = 120lx")

		dF=ser.to_frame()
		#print(dF.columns[0])

		dF['lux'] = dF[dF.columns[0]] * 120
		#dFLux.columns=['lux']
		#print(dF.columns)

		#print(dF.head())
		#print(dF['lux'].iloc[0:10])
		return dF['lux']

	'''
	convert from horizontal point to a particular vertical face

	rough conversion of light intensity for different azimuths
	east (90) = 75%
	south (180) = 100%
	west (270) = 75%
	north (0) = 10%
	'''
	def surfaceOrientationConversion(self, dFC):

		#azimuth conversation
		if self.azimuth == 0: #north
			azScaler = .1
		elif self.azimuth == 90: #east
			azScaler = .75
		elif self.azimuth == 180: #south
			azScaler = 1.0
		elif self.azimuth == 270: #west
			azScaler = .75
		print("surface conversion scaler: " + str(azScaler))

		convertedColumn = dFC * azScaler

		return convertedColumn

	#map data frame value to 0 to 255
	def convertToArduinoAnalogOutput(self,dFC, ledLuxMax):
		convertedColumn = dFC / ledLuxMax

		convertedColumnA = convertedColumn * 255

		#convertedColumnF = convertedColumnA.clip(lower=0)

		#convert to int
		#convertedColumnF = self.seriesFloor(convertedColumnA)

		#int conversation should probably happen here
		return convertedColumnA


	# concatinate series to ints - NOT REALLY WORKING YET
	def seriesFloor(self, aSeries):

		print("series floor")

		#print(aSeries.iloc[10])
		#print(math.floor(aSeries.iloc[10]))

		aSeriesL = []

		for i in range(len(aSeries)):
			aSeriesL.append(math.floor(aSeries.iloc[i]))

		aSeriesF = pd.Series(aSeriesL, name=aSeries.name)
	
		#print(aSeriesF.head())
		aSeriesF = pd.Series()
