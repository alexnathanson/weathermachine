/*This code manages communications between and control of all subsystems.
 * This is the only Arduino code necessary. Change the subsystem variable to the correct value
 * and it will automatically parse messages and run the correct code for the specified subsystem
 * 
 *For more info see the README at:
 *https://github.com/alexnathanson/weathermachine/tree/main/arduino-code 
 */

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
const int subsystem = 5;

/*** LIGHT VARIABLES ***/
const int ledPin = 9;
int ledBrightness = 0;

/*** TEA VARIABLES ***/

/*** WIND VARIABLES ***/

/*** HUMIDITY VARIABLES ****/
float RHValue = 50.0;     // Defining the humidity set point in percentage (This value will be imported from weather file)
float PlusOrMinus = 5.0;  // Defining the lower and upper set point for humidity (This value can be changed as per user...)
                          // (...settings. Below lower set point, humidifier will operate and above upper set point, dehumidifier will operate)
const int VP = A0;                    // Defining the pin for analog input through RH sensor
const int HumPin = 4, DeHumPin = 10;  // Defining the pins for digital output to control humidifier and dehumidifier operation

void setup() {
  //initialize array as all 0
  setupDeviceList();

  // Initialize I2C bus
  Wire.begin(subsystem); 
  Wire.setWireTimeout(3000, false);
  Wire.onReceive(receiveEvent); // register event
  //Wire.onRequest(requestEvent); //register event
  
  Serial.begin(9600); // Initialize serial communication

  /*** HUMIDITY VARIABLES ****/
  if(subsystem == 2){
    //lights
    pinMode(ledPin, OUTPUT);
  } else if(subsystem == 3){
    //TEA
  } else if(subsystem == 4){
    //Wind
  } else if(subsystem == 5){
    //humidity
    pinMode(HumPin, OUTPUT);            // Defining the pin for digital output to control the humidifier operation
    pinMode(DeHumPin, OUTPUT);          // Defining the pin for digital output to control the dehumidifier operation
  }
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
  
  if(subsystem == 2){
    lightLoop();
  } else if(subsystem == 3){
    teaLoop();
  } else if(subsystem == 4){
    windLoop();
  }else if(subsystem == 5){
    humidityLoop();
  }
}

void lightLoop(){
  analogWrite(ledPin, ledBrightness);
}

void teaLoop(){
  
}

void windLoop(){
  
}

/* Code for humidity subsystem*/
void humidityLoop(){
  int val, count = 40;
  float RH, avg = 0.0, volt;
  float MinLim, MaxLim;
  for (int i = 0; i < count; i++){
    val = analogRead(VP);             // Reading the voltage analog input signal (0-5V) from the RH sensor
    volt = val * 5000.0/1023.0;       // Converting the bit value of voltage analog signal to mV 
    RH = -1.92 * pow(10,-9)*pow(volt,3) + 1.44 * pow(10,-5) * pow(volt,2) + 3.4 * pow(10,-3) * volt - 12.4;
                                      // Manufacturer specified equation to convert voltage input in mV to RH in percentage
    avg += RH;                        // Adding all the RH readings to average over a period of 20s
    delay(500);                       // Adding a delay of 0.5s between recording sensor readings
  }
  avg /= count;                       // Obtaining the average RH value for the period of 20s
  if (RHValue - PlusOrMinus < 0)
    MinLim = 0;
  else
    MinLim = RHValue - PlusOrMinus;
                                      // Logic section to set the lower set point for relative humidity
  if (RHValue + PlusOrMinus > 100)
    MaxLim = 100;
  else
    MaxLim = RHValue + PlusOrMinus;
                                      // Logic section to set the lower set point for relative humidity
  if (avg <= MinLim)
    digitalWrite(HumPin, HIGH);       // Digital signal to operate the humidifier through a relay module
  else
    digitalWrite(HumPin, LOW);        // Digital signal to stop the operation of the humidifier through a relay module

  if (avg >= MaxLim)
    digitalWrite(DeHumPin, HIGH);     // Digital signal to operate the dehumidifier by powering the fuse and capacitor in ...
                                      // ... its power module
  else
    digitalWrite(DeHumPin, LOW);      // Digital signal to stop the operation of the dehumidifier by cutting the power to ...
                                      // ... the fuse and capacitor in its power module
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

void setLights(int brightness){
  Serial.print("Running Lights: ");
  Serial.println(brightness);
  ledBrightness = brightness;
  
  /*if (brightness == 0){
    digitalWrite(ledPin, LOW);
  } else {
    digitalWrite(ledPin, HIGH);
  }*/
}

void setTea(int temp){
  Serial.print("Running TEA: ");
  Serial.println(temp);
  digitalWrite(ledPin, temp);
}

void setHumidity(float humidity){
  Serial.print("Running Humidity: ");
  Serial.println(humidity);
  digitalWrite(ledPin, humidity);

  RHValue = humidity;     // Defining the humidity set point in percentage converted to float
}

void setWind(int wind){
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
        setLights(doc["lights"]);
      }
    } else if (subsystem == 3){
      if (!doc["tea"].isNull()) {
        setTea(doc["tea"]);
      }
    } else if (subsystem == 4){
      if (!doc["wind"].isNull()) {
        setWind(doc["wind"]);
      }
    } else if (subsystem == 5){
      if (!doc["hum"].isNull()) {
        setHumidity(doc["hum"]);
      }
    }

 }
