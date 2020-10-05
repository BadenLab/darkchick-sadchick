#import necessary libraries
#blynk iot
import blynklib

#adafruit
      
import board
import busio
         
import adafruit_tsl2591


#general python libraries
import time

##setup
# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
         
# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)
 
#authentication code for IOT app
BLYNK_AUTH = "***REMOVED***"

blynk = blynklib.Blynk(BLYNK_AUTH)
luxPin = 0

#WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"

# Read the total lux
def read_sensor():
    #total lux
    lux = int(sensor.lux)
    print(lux)
    blynk.set_property(luxPin, 'color', '#FF0000') 
    blynk.virtual_write(luxPin,lux)
    #wait uintill next read
    time.sleep(1.0)

while True:
    blynk.run()
    read_sensor()
