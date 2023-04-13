# import os
# import logging
from arduinoSerial import ArduinoSerial as Arduino #this is the code for communicating with an Arduino via serial
# import math
# import sys
# from threading import Thread
# from queue import Queue
from _thread import interrupt_main
import time
import serial.tools.list_ports

def run():
	global arduino

	print('')
	print("*** Testing Weather Machine ***")
	
	port = findArduino()

	print("Arduino port: " + port)

	try:
		#global arduino
		arduino = Arduino(port)
	except Exception as e:
		print(e)
		#interrupt_main()
		raise SystemExit(1)		
	
	while True:
		broadcastToArduinos(255)
		time.sleep(5)
		broadcastToArduinos(0)
		time.sleep(5)


def broadcastToArduinos(m):
	testMessage = { 'lights' : m, 'tea': m,'hum':m,'wind':m}
	arduino.sendByte(str(testMessage).encode())
	
def runAll():

	#Object that signals shutdown
	_sentinel = object()

	# q = Queue()
	# t1 = Thread(target = apiThread, args =(q, ), daemon = True)
	# t1.start()

	try:		
		run()
	except KeyboardInterrupt:
		#t1.join()
		print("Keyboard Interrupt Exception")

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
