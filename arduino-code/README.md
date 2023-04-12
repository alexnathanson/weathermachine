# Arduino I2C network

This system is composed of 5 Arduinos and a computer that acts as the test runner (TR).

The test runner is a Python program. It sends commands via Serial. 1 Arduino receives this serial data and passes it on to all the other Arduinos that run individual subsystems via I2C. The system is intended to be modular, to enable the system to run with any amount of subsystems connected and so development work can happen more easily.

Some of the individual subsystems have sensors. In some cases these sensors are just used for control feedback to maintain a certain output level, but in some cases sensor data may need to be logged. For this reason, communication in the system is bidirectional. All subsystem Arduinos can pass data back to the TR via sending it over I2C to the main Arduino, which converts it in to Serial to send to the TR. (Currently, the TR is not set up to archive this data, though that functionality could easily be added in the future.)

The TR determines what commands to send to the subsystems based on user defined test parameters (see the main README.md file for more info). The data originates from an EPW file. In order to simplify comunication and computational load on the Arduinos, the least amount and smallest dimension of data is sent to the Arduinos as possible. Some of subsystem data requires preprocessing that happens on the TR either before the test or on the fly at runtime. In some cases, the Arduino does handle a small amount of preprocessing.

Currently, the only subsystem code included is for the lights. More complex subsystem code should probably be a FROG specific library.

## Installation

Make sure to change the I2C address based on the list of subsystem addresses below.

### Adddresses

 * MAIN : 1
 * LIGHTS : 2
 * TEA : 3
 * WIND : 4
 * HUMIDITY : 5

## Subsystems

### Lights

The lights are controlled via PWM from the Arduino. There are no sensors. Preprocessing of the light data happens at the test runner and only 1 0-255 value is passed to the Arduino.

* Original data sources: Global Horizontal Radiation {Wh/m2}, Diffuse Horizontal Radiation {Wh/m2}, and Direct Normal Radiation {Wh/m2} is reduced down to 1 value based on surface orientation.
* Preprocessing on TS: Surface orientation value is scaled to the 0-255 range.
* Output from TS to Arduino: integer 0-255
* Output from Arduino to light circuit: PWM

### TEA

* Original data sources: Temperature TBD
* Preprocessing on TS: TBD
* Output from TS to Arduino: 1 temperature value
* Output from Arduino to circuit: 2 values (intensity and direction)

### Humidity


* Original data sources: humidity value TBD
* Preprocessing on TS: likely none
* Output from TS to Arduino: 1 value TBD
* Output from Arduino to circuit: TBD wind velocity and temperature

### Wind

* Original data sources: Wind velocity and direction TBD
* Preprocessing on TS: TBD - preprocessing of wind velocity + direction to get 1 value will be required
* Output from TS to Arduino: 1 value TBD
* Output from Arduino to circuit: TBD wind velocity and temperature

## Communication Protocol & Serial String Structure

### From TS to Arduino 
The TS sends all data to the Arduino network as a JSON dictionary in the following format.

`{ lights : [int 0-255], tea: [int 0-255],hum:[int 0-255],wind:[int 0-255]}`

In repeate mode, the main Arduino just sends it along.

In parse mode, the main Arduino parses the incoming message and only sends it along to the appropriate device

### From Arduino to TS

Because exact sensor data that would get sent from subsystems to TS for archiving isn't available yet, that specific format isn't finalized, but it will probably follow a similar JSON format as above, except messages would be seperated out as individual subsystems like below.

`{ tea: {temp1: [int 0-255], temp2: [int 0-255], temp3: [int 0-255]}`

## Troubleshooting

### Network status

In the Arduino IDE console, type "info" and the Arduino will respond with 
* its own I2C address
* a list of all the I2C devices and their addresses that it can detect
* the total number of I2C devices it can detect

### Message Content

In the Arduino IDE, open a console and any incoming messages from I2C should print out as they come in.

## Adding Subsystem Specific Code

## Future Work

This should be a library