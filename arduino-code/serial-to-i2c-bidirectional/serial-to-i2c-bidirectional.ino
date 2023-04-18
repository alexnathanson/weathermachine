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

const int ledPin = 9;

byte i2cDevices[128];
int nDevices = 0;

//value should correlate to i2c addressses listed above
const int subsystem = 2;

void setup() {
  //initialize array as all 0
  setupDeviceList();

  // Initialize I2C bus
  Wire.begin(subsystem); 
  Wire.setWireTimeout(3000, false);
  Wire.onReceive(receiveEvent); // register event
  //Wire.onRequest(requestEvent); //register event
  
  Serial.begin(9600); // Initialize serial communication

  pinMode(ledPin, OUTPUT);
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
    } else if (message == "test"){//run a test
      
      String testJSON = "{\"lights\":254,\"tea\":3,\"hum\":98,\"wind\":176}";
      parseJSON(testJSON);
      delay(3000);
      testJSON = "{\"lights\":0,\"tea\":0,\"hum\":0,\"wind\":0}";
      parseJSON(testJSON);

    } else {
      //Serial.println(message);

      //if broadcaster, parse serial data and broadcast it
      if(subsystem == 1){
        parseJSON(message);
      } else {
        broadcastI2C(message);//
      }
      
    }
  }
}

// function that executes whenever data is received from I2C broadcaster
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  String incomingI2C = "";//initialize string
  
  while (1 <= Wire.available()) { // loop through all bytes
    char c = Wire.read(); // receive byte as a character
    incomingI2C += c;
    //Serial.print(c);         // print the character
  }
  

  //if not the broadcaster, parse the data to do something with it
  if(subsystem != 1){
      parseJSON(incomingI2C);
      // if a subsystem, you can use this for troubleshooting in the IDE console
      //Serial.println(incomingI2C);
  } else {
    // if broadcaster, this just passes it on to the test runner
    Serial.println(incomingI2C);
  }
  //int x = Wire.read();    // receive byte as an integer
}

//this is only necessary if the Broadcaster hasn't specified an address and needs to request info
/*void requestEvent() {
  Wire.write("hello "); // respond with message of 6 bytes
}*/

void runLights(int brightness){
  Serial.print("Running Lights: ");
  Serial.println(brightness);
  
  if (brightness == 0){
    digitalWrite(ledPin, LOW);
  } else {
    digitalWrite(ledPin, HIGH);
  }
}

void runTea(int temp){
  Serial.print("Running TEA: ");
  Serial.println(temp);
  digitalWrite(ledPin, temp);
}

void runHumidity(int humidity){
  Serial.print("Running Humidity: ");
  Serial.println(humidity);
  digitalWrite(ledPin, humidity);
}

void runWind(int wind){
  Serial.print("Running Wind: ");
  Serial.println(wind);
  digitalWrite(ledPin, wind);
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
  //Serial.println(m);
  //if this is not the broadcaster, just send the data to the broadcaster.
      //in the future the input would likely not be from Serial but from the sensors
  if(subsystem != 1){
    Wire.beginTransmission(1);
    Wire.write(m.c_str()); // Send the message as a string
    Wire.endTransmission(); // End I2C transmission
  } else {//if this is the broadcaster, broadcast to all devices in the network
    for (byte address = 2; address < 127; ++address) {
      Wire.beginTransmission(address); // Replace with the I2C address of the receiving Arduino
      Wire.write(m.c_str()); // Send the message as a string
      Wire.endTransmission(); // End I2C transmission
    }        
  } 
 }

 void parseJSON(String m){
  //Serial.println("attempting to parse json");
  DynamicJsonDocument doc(200);
  String json = m;
  
  DeserializationError error = deserializeJson(doc, m);

  // Test if parsing succeeds.
  if (error) {
    //Serial.print(F("deserializeJson() failed: "));
    //Serial.println(error.f_str());
    return;
  }

  // if subsystem is 1, broadcast to everythigng
  // breakup serial into individual subsystem chunks to be small enough to send via i2c
    if(subsystem == 1){
      String lights = doc["lights"];
      if (!doc["lights"].isNull()) {
        broadcastI2C("{\"lights\":" + lights + "}");
      }
    
      String wind = doc["wind"];
      if (!doc["wind"].isNull()) {
        broadcastI2C("{\"wind\":" + wind + "}");
      }
    
      String tea = doc["tea"];
      if (!doc["tea"].isNull()) {
        broadcastI2C("{\"tea\":" + tea + "}");
      }
    
      String hum = doc["hum"];
      if (!doc["hum"].isNull()) {
        broadcastI2C("{\"hum\":" + hum + "}");
      }
    } else if(subsystem == 2){
      //check if data is meant for this particular subsystem
      if (!doc["lights"].isNull()) {
        runLights(doc["lights"]);
      }
    } else if (subsystem == 3){
      if (!doc["tea"].isNull()) {
        runTea(doc["tea"]);
      }
    } else if (subsystem == 4){
      if (!doc["wind"].isNull()) {
        runWind(doc["wind"]);
      }
    } else if (subsystem == 5){
      if (!doc["hum"].isNull()) {
        runHumidity(doc["hum"]);
      }
    }

 }
