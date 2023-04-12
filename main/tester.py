# import os
# import logging
from arduinoSerial import ArduinoSerial as Arduino #this is the code for communicating with an Arduino via serial
# import math
# import sys
from threading import Thread
from queue import Queue
from _thread import interrupt_main

import serial.tools.list_ports

#devMode = False

#arduino = object

#prints a progress bar on the console
#note that the terminal window needs to be wide enough to fit all text otherwise it will look wierd
def progressBar(iteration, total, prefix = 'Progress', suffix = 'Complete', suffix2 = 'Min Remaining', decimals = 1, length = 100, fill = '█', printEnd = "\r"):

    #prefix = "Progress"
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	estMin = total - iteration
	print(f'\r{prefix} |{bar}| {iteration}% {suffix} {estMin} {suffix2}', end = printEnd)
	
	if iteration == 100:
		print()

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
	
	arduino.sendByte(str('testing python').encode())
	
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
