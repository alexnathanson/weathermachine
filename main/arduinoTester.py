# import os
# import logging
from arduinoSerial import ArduinoSerial as Arduino #this is the code for communicating with an Arduino via serial
# import math
# import sys
from threading import Thread
from queue import Queue
from _thread import interrupt_main
import time
import serial.tools.list_ports
import random

def testArduinos():
	port = findArduino()

	print("Arduino port: " + port)

	try:
		arduino = Arduino(port)
	except Exception as e:
		print(e)
		#interrupt_main()
		raise SystemExit(1)		

	#m=255
	#random.seed(10)
	while True:
		for i in range(0,6):
			m = 50 * i
			testMessage = { 'lights' : m, 'tea': m,'hum':m,'wind':m}
			arduino.sendByte(str(testMessage).encode())
			#m = int(random.random() * 255)

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
