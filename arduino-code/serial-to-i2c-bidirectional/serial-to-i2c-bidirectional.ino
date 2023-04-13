/*
 * I2C Addresses:
 * BROADCASTER : 1
 * LIGHTS : 2
 * TEA : 3
 * WIND : 4
 * HUMIDITY : 5
 */

#include <Wire.h>
#include <ArduinoJson.h>


byte i2cDevices[128];
int nDevices = 0;

//value should correlate to i2c addressses listed above
const int subsystem = 1;
 
void setup() {
  //initialize array as all 0
  setupDeviceList();

  // Initialize I2C bus
  Wire.begin(subsystem); 
  Wire.setWireTimeout(3000, false);
  Wire.onReceive(receiveEvent); // register event
  //Wire.onRequest(requestEvent); //register event
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  // Read serial input and send it over I2C
  if (Serial.available()) {
    String message = Serial.readStringUntil('\n'); // Read serial message until newline character

    //respond to the info request with your own info
    if (message == "info"){
      Serial.println("***INFO***");
      Serial.println("My address is " + String(subsystem));
      scannerI2C();
    } else {
      Serial.println(message);
      //if this is not the broadcaster, just send the data to the broadcaster.
      //in the future the input would likely not be from Serial but from the sensors
      if(subsystem != 1){
        Wire.beginTransmission(1);
        Wire.write(message.c_str()); // Send the message as a string
        Wire.endTransmission(); // End I2C transmission
      } else {//if this is the broadcaster, broadcast to all devices in the network
        broadcastI2C(message);         
      } 
    }
  }

}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  while (1 <= Wire.available()) { // loop through all bytes
    char c = Wire.read(); // receive byte as a character
    Serial.print(c);         // print the character
  }
  Serial.println();
  //int x = Wire.read();    // receive byte as an integer
}

//this is only necessary if the main controller hasn't specified an address and needs to request info
//if the main controller has an identified address
void requestEvent() {
  Wire.write("hello "); // respond with message of 6 bytes
  // as expected by master
}

void lights(int brightness){
  const int ledPin = 13;

  analogWrite(ledPin, brightness);
}
void setupDeviceList(){
  for (byte d = 0; d < 128; ++d) {
    i2cDevices[d]=0;  
  }  
}

//scan for all connected i2c devices
void scannerI2C(){
  nDevices = 0;
  
  for (byte address = 1; address < 127; ++address) {
    // The i2c_scanner uses the return value of the Wire.endTransmission
    //to see if a device did acknowledge to the address.
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      Serial.println(address, HEX);
      i2cDevices[nDevices]=address;
      nDevices = ++nDevices;
    } else if (error == 4) {
      Serial.print("Unknown error at address 0x");
      Serial.println(address, HEX);
      i2cDevices[nDevices]=0;
    } else {
      i2cDevices[nDevices]=0;
    }
  }
  
  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
  } else {
    Serial.print(nDevices, DEC);
    Serial.println(" I2C devices found.");

    //print location of devices
    Serial.println('\n');
  }

 }

 //broadcast message to all connected i2c devices
 //there may be a more elegant way to do this with sending to the 0 address
void broadcastI2C(String m){
  for (byte address = 2; address < 127; ++address) {
    Wire.beginTransmission(address); // Replace with the I2C address of the receiving Arduino
    Wire.write(m.c_str()); // Send the message as a string
    Wire.endTransmission(); // End I2C transmission
  }
 }
