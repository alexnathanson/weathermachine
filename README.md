# weathermachine

All the code for controlling the system from a centralized computer/ server is in main

To run:

`python main`


To do:

smooth numbers over time
timing

Troubleshooting:

If you get a serial error, make sure to close all Arduino windows to ensure that only Python is communicating via Serial



clean data is defined here as data with 1 single row of headers.
it does not necessarily mean there aren't problems in the data

HEADERS:
Date
HH:MM
Datasource
Dry Bulb Temperature {C}
Dew Point Temperature {C}
Relative Humidity {%}
Atmospheric Pressure {Pa}
Extraterrestrial Horizontal Radiation {Wh/m2}
Extraterrestrial Direct Normal Radiation {Wh/m2}
Horizontal Infrared Radiation Intensity from Sky {Wh/m2}
Global Horizontal Radiation {Wh/m2}
Direct Normal Radiation {Wh/m2}
Diffuse Horizontal Radiation {Wh/m2}
Global Horizontal Illuminance {lux}
Direct Normal Illuminance {lux}
Diffuse Horizontal Illuminance {lux}
Zenith Luminance {Cd/m2}
Wind Direction {deg}
Wind Speed {m/s}
Total Sky Cover {.1}
Opaque Sky Cover {.1}
Visibility {km}
Ceiling Height {m}
Present Weather Observation
Present Weather Codes
Precipitable Water {mm}
Aerosol Optical Depth {.001}
Snow Depth {cm}
Days Since Last Snow
Albedo {.01}
Liquid Precipitation Depth {mm}
Liquid Precipitation Quantity {hr}
