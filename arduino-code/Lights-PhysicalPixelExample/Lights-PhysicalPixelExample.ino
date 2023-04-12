/*
  Based off of the Physical Pixel and Dimmer Examples

  
*/
//const int ledPinA = 6; // the pin that the LED is attached to

const int ledPinB = 13; // the pin that the LED is attached to
char sendHello[] = " Hello From Arduino Uno";
char dataConfirmed[] = "Arduino got data";

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  // initialize the LED pin as an output:
  //pinMode(ledPinA, OUTPUT);
  pinMode(ledPinB, OUTPUT);

  Serial.println(sendHello); // sends a \n with text
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

  }

  //delay(10);
}
