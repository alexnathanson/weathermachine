/*
  Based off of the Physical Pixel and Dimmer Examples


  created 2006
  by David A. Mellis
  modified 30 Aug 2011
  by Tom Igoe and Scott Fitzgerald

  
  An example of using the Arduino board to receive data from the computer. In
  this case, the Arduino boards turns on an LED when it receives the character
  'H', and turns off the LED when it receives the character 'L'.

*/

const int ledPin = 13; // the pin that the LED is attached to
int incomingByte;      // a variable to read incoming serial data into
char TextToSend[] = " Hello From Arduino Uno";
char dataConfirmed[] = "Arduino got data";

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);

  
  Serial.println(TextToSend); // sends a \n with text
}

void loop() {
  byte brightness;
    //analogWrite(ledPin, incomingByte);
  //Serial.println(dataConfirmed); // sends a \n with text

  // check if data has been sent from the computer:
  if (Serial.available() > 0) {
    // read the most recent byte (which will be from 0 to 255):
    brightness = Serial.read();
    //Serial.println(dataConfirmed); // sends a \n with text
    //incomingByte = 255;
    // set the brightness of the LED:
    digitalWrite(ledPin, brightness);
  }

  delay(10);
}
