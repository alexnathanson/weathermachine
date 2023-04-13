# import os
import logging
from arduinoSerial import ArduinoSerial as Arduino #this is the code for communicating with an Arduino via serial
# import math
# import sys
from threading import Thread
#from queue import Queue
from _thread import interrupt_main
import time
import serial.tools.list_ports
import random
from datetime import datetime
import logging

logging.basicConfig(filename='main/logs/tester' + datetime.now().strftime("%Y-%m-%d-%H-%M") +'.log',  level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info('tester running!')

def testArduinos():
	port = findArduino()

	print("Arduino port: " + port)

	try:
		arduino = Arduino(port)
	except Exception as e:
		print(e)
		#interrupt_main()
		raise SystemExit(1)		

	tempData = ''
	while True:
			if tempData != arduino.serialData:
				tempData = arduino.serialData
				logging.info(tempData)

			testMessage = { 'lights' : 255, 'tea': 16,'hum':100,'wind':16}
			arduino.sendByte(str(testMessage).encode())
			#m = int(random.random() * 255)

			time.sleep(3)

			testMessage = { 'lights' : 0, 'tea': 0,'hum':0,'wind':0}
			arduino.sendByte(str(testMessage).encode())
		
			time.sleep(3)

	
def runAll():

	#Object that signals shutdown
	_sentinel = object()

	try:		
		#run()
		print('')
		print("*** Testing Weather Machine ***")
		
	
		#q = Queue()
		aT = Thread(target = testArduinos)
		aT.start()

	except KeyboardInterrupt:
		#t1.join()
		print("Keyboard Interrupt Exception")

		#turn off the arduino outputs if possible
		try:
			arduino.turnOff()
		except:
			pass
		raise SystemExit(1)

def findArduino():
	print("Searching for connected Arduino")
	ports = list(serial.tools.list_ports.comports())
	aPort = ''

	try:
		for p in ports:
			if "Arduino" in p.description:
				aPort = p.name 
				break

		if aPort == '':
			print("Arduino not detected")
		else:
			print("Arduino detected on port " + aPort)
			return aPort
	except:
			print("Arduino not detected")

if __name__ == '__main__':
	runAll()
