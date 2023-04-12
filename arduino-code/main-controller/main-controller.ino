/*
  This code receives serial data from the test runner via Serial (USB) to control weather machine outputs.
  It detects remote devices connected via I2C and passes all incoming serial data to all remote devices
  The remote devices may have sensor data, which they all pass on to this script, which passes it back to the test runner.

  The exact data formats are TBD  
*/

//this is for I2C communication between Arduinos
#include <Wire.h>

int i2cDevices[128];

const int ledPinB = 13; // the pin that the LED is attached to
char sendHello[] = " Hello From Arduino Uno";
char dataConfirmed[] = "Arduino got data";

#define ARRAY_SIZE(array) ((sizeof(array))/(sizeof(int)))

void setup() {
  Wire.begin();
  // initialize serial communication:
  Serial.begin(9600);
  // initialize the LED pin as an output:
  //pinMode(ledPinA, OUTPUT);
  pinMode(ledPinB, OUTPUT);

  Serial.println(sendHello); // sends a \n with text

  scannerI2C();
}

void loop() {
  int brightness;

  // check if data has been sent from the computer:
  if (Serial.available() > 0) {
    // read the most recent byte (which will be from 0 to 255):
    brightness = Serial.parseInt();
    Serial.println(String(brightness)); // sends a \n with text
    // set the brightness of the LED:
    //analogWrite(ledPinA, brightness);
    analogWrite(ledPinB, brightness);

    repeaterI2c(String (brightness));
  }

  delay(10);
}

//repeat all serial messages to all devices connected via I2C
void repeaterI2c(String message){

  //convert String to chars
  char buffer[ARRAY_SIZE(message)];
  
  message.toCharArray(buffer, 32);
  
  for (byte address = 0; address < ARRAY_SIZE(i2cDevices); ++address){
      Wire.beginTransmission(i2cDevices[address]); // transmit to devices
      Wire.write(buffer);        // sends message
      Wire.endTransmission();    // stop transmitting

    }
}

//scan for I2C devices on start up
void scannerI2C(){
  int nDevices = 0;
  Serial.println("Scanning for I2C devices...");

  for (byte address = 1; address < 127; ++address) {
    // The i2c_scanner uses the return value of
    // the Wire.endTransmission to see if
    // a device did acknowledge to the address.
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      /*if (address < 16) {
        Serial.print("0");
      }*/
      Serial.print(address, HEX);
      Serial.println(" !");
      i2cDevices[nDevices]=address;
      nDevices = ++nDevices;
    } else if (error == 4) {
      Serial.print("Unknown error at address 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.println(address, HEX);
    }
  }
  
  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
  } else {
    Serial.print(nDevices, DEC);
    Serial.println(" I2C devices found:");

    //print location of devices
    for (byte address = 0; address < ARRAY_SIZE(i2cDevices); ++address){
      Serial.print(i2cDevices[address], DEC);
      Serial.print(' ');
    }
    Serial.println('\n');
  }
}
