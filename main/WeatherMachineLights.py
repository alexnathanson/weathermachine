#this code is for the weather machine's lighting elements


class WMLights:
	def __init__(self, azimuth):
		self.azimuth = azimuth

	#convert Wh/m2 to Lux
	def energyToLux(self, dF):
		print("energy to lux converion")
		return dF

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
	# NOT TESTED
	def convertToArduinoAnalogOutput(self,dFC, dfMin, dfMax):
		scaler = (dfMax - dfMin) / 255
		convertedColumn = dFC * scaler
		return convertedColumn