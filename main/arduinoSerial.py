import serial
import time

class ArduinoSerial():
    def __init__(self, aPort):
        self.port = aPort
        self.baud = 9600
        if self.port != 'DEVMODE':
            self.serialObj = serial.Serial(self.port)
            print("Arduino Serial connection starting...")
            time.sleep(3)
            self.receivedString = self.serialObj.readline()
            print(self.receivedString.decode("utf-8") )
            self.devmode = False
        else:
            self.devmode = True
            print("Running in DEVMODE with no Arduino")

#arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data

# while True:
#     num = input("Enter a number: ") # Taking input from user
#     value = write_read(num)
#     print(value) # printing the value
    
    def turnOff(self):
        if not self.devmode:
            self.serialObj.write(str(0).encode()) 

    def sendByte(self,theByte):
        #with serial.Serial(self.port, self.baud, timeout=1) as ser:
            #time.sleep(0.5)
        #print("byte: " + str(theByte))
        if not self.devmode:
            self.serialObj.write(theByte)   # send the pyte string 'H'
            #time.sleep(0.5)   # wait 0.5 seconds
            #ser.write(b'L')   # send the byte string 'L'