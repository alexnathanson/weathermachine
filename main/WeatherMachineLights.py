#this code is for the weather machine's lighting elements

import pandas as pd
import math
from datetime import datetime

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
	def detailedSurfaceOrientation(self, dfOr):

		HGloHor = dfOr['Global Horizontal Radiation {Wh/m2}']
		DifHor = dfOr['Diffuse Horizontal Radiation {Wh/m2}']
		HDirNor = dfOr['Direct Normal Radiation {Wh/m2}']

		#δ declination angle
		#date str to time
		dfOr['Date Format'] = dfOr['Date'].apply(self.strToDateTime)
		#date to day number
		dfOr['Day num'] = dfOr['Date Format'].apply(self.dateToDayNumber)
		dfOr['declination'] = dfOr['Day num'].apply(self.declinationAngle)

		#ω solar hour
		dfOr['HH'] = dfOr['HH:MM'].apply(self.hhmmTohh)
		dfOr['solar hour'] = dfOr['HH'].apply(self.solarHour)
		
		sOmega = dfOr['solar hour']
		sDelta = dfOr['declination']
		print(type(sDelta))

		omSin =dfOr['solar hour'].apply(math.sin)
		omCos = dfOr['solar hour'].apply(math.cos)

		#print(sDelta.head())
		delSin = dfOr['declination'].apply(math.sin)
		delCos = dfOr['declination'].apply(math.cos)

		#ϕ 
		# should this get passed in with azimuth?
		sLat = 41

		if self.azimuth == 0: #north
			sTheta = (delSin * math.cos(sLat) - delCos * math.sin(sLat) * omCos).apply(math.asin) 

			#Therefore, hourly total solar irradiation on the wall is:
			sIr = 0.5*HGloHor*0.2 + 0.5*DifHor + HDirNor* sTheta.apply(math.cos)

		elif self.azimuth == 90: #east
			sTheta = ( - delCos * omSin).apply(math.asin)
			sIr = 0.5*HGloHor*0.2 + 0.5*DifHor + HDirNor*sTheta.apply(math.cos)

		elif self.azimuth == 180: #south

			sTheta = (-delSin * math.cos(sLat) + delCos * math.sin(sLat) * omCos).apply(math.asin)
			sIr = 0.5*HGloHor*0.2 + 0.5*DifHor + HDirNor*sTheta.apply(math.cos)

		elif self.azimuth == 270: #west

			sTheta = (delCos * omSin).apply(math.asin)
			sIr = 0.5*HGloHor*0.2 + 0.5*DifHor + HDirNor*sTheta.apply(math.cos)

		elif self.azimuth == 'roof':
			sTheta = (delSin * math.Sin(sLat) + delCost * math.cos(sLat) * omCos).apply(math.asin)
			sIr = HGloHor + HDirNor*sTheta.apply(math.cos)

		dfOr['surface irradiance'] = sIr

		#print(dfOr.iloc[0:20])

		return dfOr['surface irradiance']

	def detailedSurfaceOrientationConversion(self):
		if self.azimuth == 0: #north
			sTheta = math.asin(math.sin(sDelta) * math.cos(sLat) - math.cos(sDelta) * math.sin(sLat) * math.cos(sOmega)) 

			#Therefore, hourly total solar irradiation on the wall is:
			sIr = 0.5*HGloHor*0.2 + 0.5*DifHor + HDirNor*math.cos(sTheta)

		elif self.azimuth == 90: #east
			sTheta = math.asin ( - math.cos(sDelta) * math.sin(sOmega))
			sIr = 0.5*HGloHor*0.2 + 0.5*DifHor + HDirNor*math.cos(sTheta)

		elif self.azimuth == 180: #south

			sTheta = math.asin(-math.sin(sDelta) * math.cos(sLat) + math.cos(sDelta) * math.sin(sLat) * math.cos(sOmega))
			sIr = 0.5*HGloHor*0.2 + 0.5*DifHor + HDirNor*math.cos(sTheta)

		elif self.azimuth == 270: #west

			sTheta = math.asin(math.cos(sDelta) * math.sin(sOmega))
			sIr = 0.5*HGloHor*0.2 + 0.5*DifHor + HDirNor*math.cos(sTheta)

		# elif self.azimuth == 'roof':
		# 	sTheta = math.asin (sin δ sin ϕ + cos δ cos ϕ cos ω)
		# 	sIr = HGloHor + HDirNor*cos(sTheta)

		return sIr

	def strToDateTime(self,dT):
		return datetime.strptime(dT, '%m/%d/%Y').date()

	#convert hours:minutes to just hours
	def hhmmTohh(self,hhmm):
		return int(hhmm.split(':')[0])

	# δ = -0.4092cos(2π/365*(d+10)), where d is the day of year (such that d= 1 on Jan 1)
	def declinationAngle(self, dayNum):
		return -0.4092 * math.cos(2* math.pi/365*(dayNum+10))

	# ω = π/12*(t-12), where t is the local solar time in hours
	def solarHour(self, sTime):
		return math.pi/12*(sTime-12)

	#convert datetime formmated date to day of the year
	# we could also just divide by 24 but that might mess things up when we ease the middle ranges later
	def dateToDayNumber(self,aDate):
		return aDate.timetuple().tm_yday

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