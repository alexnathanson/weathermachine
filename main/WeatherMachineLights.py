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
	# returns a series
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
	roughly convert from horizontal point to a particular vertical face

	rough conversion of light intensity for different azimuths
	east (90) = 75%
	south (180) = 100%
	west (270) = 75%
	north (0) = 10%
	'''
	def roughSurfaceOrientationConversion(self, dFC):

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


	'''
	detailed conversion from horizontal point to a particular vertical face
	equations from Youngjin Hwang
	https://docs.google.com/document/d/11sM10-iicSdTeooRDKgKW0v6Aa3aOrDD/edit?usp=sharing&ouid=114681549877036963956&rtpof=true&sd=true
	'''
	# def detailedSurfaceOrientation(self):
	# 	if self.azimuth == 0: #north
	# 		#θ’n = arcsin (sin δ cos ϕ − cos δ sin ϕ cos ω) 

	# 		#Therefore, hourly total solar irradiation on the wall is:
	# 		#0.5*HGloHor*0.2 + 0.5*DifHor + HDirNor*cos(θ’n)

	# 	elif self.azimuth == 90: #east
	# 		azScaler = .75
	# 	elif self.azimuth == 180: #south
	# 		azScaler = 1.0
	# 	elif self.azimuth == 270: #west
	# 		azScaler = .75
	# 	print("surface conversion scaler: " + str(azScaler))

	# 	convertedColumn = dFC * azScaler

	# 	return convertedColumn

	# δ = -0.4092cos(2π/365*(d+10)), where d is the day of year (such that d= 1 on Jan 1)
	def declinationAngle(self, dayNum):
		return -0.4092 * math.cos(2* math.pi/365*(dayNum+10))

	# ω = π/12*(t-12), where t is the local solar time in hours
	def solarHour(self, sTime):
		return math.pi/12*(sTime-12)

	'''
	map data frame value to 0 to 255
	returns a series
	'''
	def convertToArduinoAnalogOutput(self,dFC, ledLuxMax):
		convertedColumn = dFC / ledLuxMax

		convertedColumnA = convertedColumn * 255

		#convertedColumnF = convertedColumnA.clip(lower=0)

		#convert to int
		#convertedColumnF = self.seriesFloor(convertedColumnA)

		#int conversation should probably happen here
		return self.seriesFloor(convertedColumnA)


	# concatinate series of floats to ints
	def seriesFloor(self, aSeries):

		aSeriesL = []

		for i in range(len(aSeries)):
			aSeriesL.append(math.floor(aSeries.iloc[i]))

		aSeriesF = pd.Series(aSeriesL, name=aSeries.name)

		return aSeriesF