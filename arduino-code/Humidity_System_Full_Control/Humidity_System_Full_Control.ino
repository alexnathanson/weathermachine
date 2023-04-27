float RHValue = 50.0;     // Defining the humidity set point in percentage (This value will be imported from weather file)
float PlusOrMinus = 5.0;  // Defining the lower and upper set point for humidity (This value can be changed as per user...)
                          // (...settings. Below lower set point, humidifier will operate and above upper set point, dehumidifier will operate)

const int VP = A0;                    // Defining the pin for analog input through RH sensor
const int HumPin = 4, DeHumPin = 10;  // Defining the pins for digital output to control humidifier and dehumidifier operation

void setup() {
  Serial.begin(9600);
  pinMode(HumPin, OUTPUT);            // Defining the pin for digital output to control the humidifier operation
  pinMode(DeHumPin, OUTPUT);          // Defining the pin for digital output to control the dehumidifier operation
}

void loop() {
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
