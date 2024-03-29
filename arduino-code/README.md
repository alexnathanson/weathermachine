# Arduino I2C network

This system is composed of 5 Arduinos and a computer that acts as the test runner (TR).

The test runner is a Python program. It sends commands via Serial. 1 Arduino receives this serial data and passes it on to all the other Arduinos that run individual subsystems via I2C. The system is intended to be modular, to enable the system to run with any amount of subsystems connected and so development work can happen more easily.

Some of the individual subsystems have sensors. In some cases these sensors are just used for control feedback to maintain a certain output level, but in some cases sensor data may need to be logged. For this reason, communication in the system is bidirectional. All subsystem Arduinos can pass data back to the TR via sending it over I2C to the broadcaster Arduino, which converts it in to Serial to send to the TR.

The TR determines what commands to send to the subsystems based on user defined test parameters (see the main README.md file for more info). The data originates from an EPW file. In order to simplify comunication and computational load on the Arduinos, the least amount and smallest dimension of data is sent to the Arduinos as possible. Some of subsystem data requires preprocessing that happens on the TR either before the test or on the fly at runtime. In some cases, the Arduino does handle a small amount of preprocessing.

The only piece of code necessary is the serial-to-i2c-bidirectional-subsystem-control.ino script. Change the subsystem variable to the correct number and the Arduino will automatically parse messages and run the correct subsystem. (Currently, the only subsystem code included is for the lights and humidity systems.)

## Installation of serial-to-i2c-bidirectional-subsystem-control.ino

### Software

Make sure to change the I2C address based on the list of subsystem addresses below.

Install Arduino Json https://arduinojson.org/v6/doc/installation/

### Wiring

All Arduinos are connected together via pins GND, A4, and A5. Note that if Arduinos share a power supply with a common ground, the GND pin connection isn't necessary.

<img src="/hardware-documentation/wiring/ArduinoNetworkWiring.png">

### Adddresses

 * BROADCASTER : 1
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

### From TS to Broadcaster via Serial
The TS sends all data to the Arduino network as a JSON dictionary in the following format. Regardless of what subsystem info is include, all data is broadcast to the entire network. This can be changed in the future if it leads to problems.

`{ lights : [int 0-255]}`

or for multiple values: 

`{ lights : [int 0-255], tea: [int 0-255],hum:[int 0-255],wind:[int 0-255]}`

### Broadcaster On receiving Serial:

1) parse JSON
2) break up JSON data by subsystem
3) broadcast all data to all devices

### Broadcaster on receiving I2C:

1) pass incoming data to Serial

### Subsystems on receiving Serial:

1) send to Broadcaster via 12C

### Subsystems on receiving I2C:

1) parse incoming JSON data
2) check if data is intended for the particular subsystem
3) if yes, run run system functions

### From Arduino to TS

Because exact sensor data that would get sent from subsystems to TS for archiving isn't available yet, that specific format isn't finalized, but it will probably follow a similar JSON format as above, except messages would be seperated out as individual subsystems like the below theoretical example with 3 different temperature sensors. As with communication in the other direction, it is best to reduce the dimension of data if possible. So in this example, unless you need to archive all 3 pieces of data it would be best to just send an average.

`{ tea: {temp1: [int 0-255], temp2: [int 0-255], temp3: [int 0-255]}`

## Troubleshooting

### Network status

In the Arduino IDE console, type "info" and the Arduino will respond with 
* its own I2C address
* a list of all the I2C devices and their addresses that it can detect
* the total number of I2C devices it can detect

In the Arduino IDE console, type "test" and the Arduino will send a properly formatted I2C message with 0 values

### Message Content

In the Arduino IDE, open a console and any incoming messages from I2C should print out as they come in.

## Adding Subsystem Specific Code

## Future Work

It might be best to have 1 library that encompasses all network functions and subsystem functions so that each Arduino can have identical software running.
