# darkchick-sadchick
Light sensor to detec circadian rythm failures


This system is composed of:
Hardware
1 - raspberry pi zero
2 - TSL2591 Adafruit sensor - has a range of 88000 lux

software:
1 - circuit Python running on the Pi
2 - Blinky for an mobile app


The idea of this project is pretty straight forward. Light sensor detects lux and python on the RPI counts time. this logs data every 10 min or so and sends it to a mobile app.
If the light is off or on for longer than it is supposed to, it sends an "alarm" to the mobile app.


### this system is currently before alpha, so proceed with care.


Documentation (links with tutorials used to put this together)

Adatfruit sensor  and how to wire it to the Pi GPIO https://learn.adafruit.com/adafruit-tsl2591/python-circuitpython


Getting SSH on the RPi without having to have a monitor and keyboard (information "injected" directly on SD card before first boot) https://www.raspberrypi.org/documentation/remote-access/ssh/unix.md


Getting the RPI connected without keyboard, mouse and monitor (information injected directly on SD card) https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

Install Circuit Python on the RPi https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

Install the library for the sensor https://github.com/adafruit/Adafruit_CircuitPython_TSL2591

Once you have setup everything on the Pi, and made sure the example code from Adafruit works, we need to move to the Blynk.io side of things https://blynk.io/

This is the platform that will allow data from the Pi to be transmitted over the web and to the users mobile phone app. This is only free for up to 5 projects, but since we need something quick and easy, this will do.

Check their get-started page to start https://blynk.io/en/getting-started


