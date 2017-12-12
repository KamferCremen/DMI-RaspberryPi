import sys
import time
import datetime
import Adafruit_DHT as dht
import json
import requests
import smbus
import RPi.GPIO as GPIO
import threading
from threading import Thread

def light_func():

    bus = smbus.SMBus(1)
    bus.write_byte(0x48, 0x00)

    while (True):

        measure = bus.read_byte(0x48)

        while (measure > 240):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.OUT)
            measure = bus.read_byte(0x48)
            GPIO.output(18, GPIO.HIGH)
            time.sleep(1)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, GPIO.LOW)
        GPIO.cleanup()
        time.sleep(1)



def temp_func():
    while(True):

        timer = time.time()

        while(time.time() - timer < 3600): # 1 hour

            time.sleep(5)
            error_file = open("errorlog.txt", "a")

            humidity, temperature = dht.read_retry(dht.DHT22, 22)

            try:
                url = 'http://dmiprivateservices.azurewebsites.net/DMIService.svc/temperatures/live?temp={0:.2f}'.format(float(temperature))
                response = requests.get(url)

                print("\r\nLIVE\r\nTemp : {0} \r\nStatus : {1} ".format(float(temperature), response.status_code))

            except Exception as e:
                error_file.write(
                    "\r\nLive Error \r\nTime : {0} \r\nTemp : {1} \r\nError : {2} \r\r\n".format(datetime.date.today(), temperature, e))
                    #dont want to write every 5 sec data into the log, only when live crashes

            error_file.close()


        log_file = open("datalog.txt", "a")
        error_file = open("errorlog.txt", "a")
        humidity, temperature = dht.read_retry(dht.DHT22, 22)

        try:
            url = 'http://dmiprivateservices.azurewebsites.net/DMIService.svc/temperatures'
            data = {"Temperature" : "{0:.2f}".format(float(temperature))}
            data_json = json.dumps(data)
            headers = {'Content-type': 'application/json'}
            response = requests.post(url, data=data_json, headers=headers)

            print("\r\nHOURLY\r\nTemp : {0} \r\nStatus : {1} ".format(float(temperature), response.status_code))

            log_file.write(
             "\r\nTime : {0} \r\nStatus : {1} \r\nData : {2} \r\r\n".format(datetime.date.today(), response.status_code,
                                                                            data_json))
        except Exception as e:
            error_file.write("\r\nTime : {0} \r\nTemp : {1} \r\nError : {2} \r\r\n".format(datetime.date.today(), temperature, e))

        error_file.close()
        log_file.close()


try:
    Thread(target = temp_func).start()
    Thread(target = light_func).start()

except:
    print("Threading failed...")




