#import necessary libraries
#blynk iot
import blynklib

#adafruit
      
import board
import busio
import csv

import adafruit_tsl2591
import adafruit_dht


#general python libraries
import time
import datetime

##setup
# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
         
# Initialize the sensor.
luxSensor = adafruit_tsl2591.TSL2591(i2c)

#create an object for the DHT temperature and humidity sensor
#right now this is connected to gpio pin 18
dhtSensor = adafruit_dht.DHT11(board.D18)
#authentication code for IOT app
BLYNK_AUTH = "***REMOVED***"

blynk = blynklib.Blynk(BLYNK_AUTH)
luxPin  = 0
tempPin = 1
humPin  = 2

isDark = False
#WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"

# Read the total lux
def read_sensors():
    #total lux
    lux = luxSensor.lux
    try:
        temperature = dhtSensor.temperature
        humidity = dhtSensor.humidity
    except RuntimeError:
        print("something wrong with DHT!")
        temperature = -273
        humidity = -100

    print("lux: " + str(lux))
    print("temperature: "+str(temperature))
    print("humidity: "+str(humidity))
    print("----\n")

    #set lux to RED
    #blynk.set_property(luxPin, 'color', '#FF0000')
    blynk.virtual_write(luxPin,lux)
    blynk.virtual_write(tempPin,temperature)
    blynk.virtual_write(humPin,humidity)


    return lux, temperature, humidity


def get_daytime():

    now = datetime.datetime.now()                                           
    #here we set the time we want to compare things against. 
    #lights are on at 10:00 am in the AU, we set the time to 10:30, to give it a "grace period" for clocks async, etc.
    today10am = now.replace(hour=10,minute=30,second=0,microsecond=0) 
    today10pm = now.replace(hour=22,minute=0,second=0,microsecond=0) 
    yesterday10pm = now.replace(hour=22,minute=0,second=0,microsecond=0,day=now.day-1)
    tomorrow10am = now.replace(hour=10,minute=30,second=0,microsecond=0,day=now.day+1)
    # we also need to mark the time for tomorrow 10 am, so that we check that the room is dark when it is supposed too.


    return now, today10am, today10pm, tomorrow10am,yesterday10pm

csvPath = "/home/pi/Documents/"
csvFile = "chickenRoomData.csv"

#check to see if file already exists, in which case there is no need to add the header again
try:
    with open(csvPath+csvFile) as f:
        header = False
        # Do something with the file
except IOError:
    header = True

counter1 = 0
notifyDark = 0
notifyDarkCounter = 0
notifyLight = 0
notifyLightCounter = 0

#run forever
while True:
    blynk.run()
    lux,temperature,humidity = read_sensors()

    timeNow= datetime.datetime.now()
    #to avoid writing too much data to the CSV, we only record 1 in 120 readings.
    #we need "many" readings, because otherwise the blynk app sees the rpi as disconnected.
    #this is why there is this " if counter " component here
    if counter1 == 0:
        with open(csvPath+csvFile,mode = 'a') as chickCSV:
            fieldnames = ['date', 'lux', 'temperature','humidity']
            writer = csv.DictWriter(chickCSV, fieldnames=fieldnames)
            if header is True:
                writer.writeheader()
                header = False

            writer.writerow({'date': str(timeNow), 
                         'lux': str(lux), 
                         'temperature': str(temperature),
                         'humidity':str(humidity)})
        
    now, today10am, today10pm, tomorrow10am, yesterday10pm = get_daytime()
    #print(today10am)
    #print(today10pm)
    #print(tomorrow10am)
    #print(yesterday10am)
    
    if now>today10am and now<today10pm and lux<100:
        print("lights should be on")
        notifyDarkCounter = notifyDarkCounter + 1
        if notifyDarkCounter == 720:
            notifyDarkCounter = 0
            notifyDark = 1
    
    if now>yesterday10pm and now<today10am and lux>100:
        print("lights should be off")
        notifyLightCounter = notifyLightCounter + 1
        if notifyLightCounter == 720:
            notifyLightCounter = 0
            notifyLight = 1

    if now>today10pm and now<tomorrow10am and lux>100:
        print("lights should be off")
        notifyLightCounter = notifyLightCounter + 1
        #only send an email if the problem is there for more at least hour
        if notifyLightCounter == 720:
            notifyLightCounter = 0
            notifyLight = 1

    

    counter1 = counter1 + 1
    if counter1 == 120:
        counter1 = 0
    if notifyDark == 1:
        blynk.notify('chickens are now in the dark! They must be sad!')
        blynk.email(to="am2106@sussex.ac.uk",subject="chickenroom",body= "lights off when they should be on!")
        notifyDark = 0
    if notifyLight == 1:
        #print("lights should be off! /n")
        blynk.email(to="am2106@sussex.ac.uk",subject="chickenroom",body="lights on when they should be off!")
        blynk.notify("lights are on! Chickens must be raving!!")
        notifyLight = 0



    #count time and put things to sleep while waiting
    time.sleep(5.0)
