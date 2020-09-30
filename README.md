# darkchick-sadchick
Light sensor to detec circadian rythm failures


This system is composed of:
Hardware
1 - raspberry pi zero
2 - TSL2591 Adafruit sensor

software:
1 - circuit Python running on the Pi
2 - Blinky for an mobile app


The idea of this project is pretty straight forward. Light sensor detects lux and python on the RPI counts time. this logs data every 10 min or so and sends it to a mobile app.
If the light is off or on for longer than it is supposed to, it sends an "alarm" to the mobile app.


### this system is currently before alpha, so proceed with care.
