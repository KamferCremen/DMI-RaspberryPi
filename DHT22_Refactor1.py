import sys
import time
import datetime
import Adafruit_DHT as dht
import json
import requests

counter = 0 #only for testing, to limit amount of loops

while(counter != 2): #change to true once testing is done

 time.sleep(1) #sleeps for 1 hour, 3600sec, before finishing loop

 humidity, temperature = dht.read_retry(dht.DHT22, 22)
 log_file = open("datalog.txt", "a")
 error_file = open("errorlog.txt", "a")

 try:
     url = 'http://dmiprivateservices.azurewebsites.net/DMIService.svc/temperatures'
     data = {"Temperature" : "{0:.2f}".format(float(temperature))}
     data_json = json.dumps(data)
     headers = {'Content-type': 'application/json'}
     response = requests.post(url, data=data_json, headers=headers)

     print(float(temperature))
     print(response.status_code)

     log_file.write(
         "\r\nTime : {0} \r\nStatus : {1} \r\nData : {2} \r\r\n".format(datetime.date.today(), response.status_code,
                                                                        data_json))

 except Exception as e:
     error_file.write("\r\nTime : {0} \r\nTemp : {1} \r\nError : {2} \r\r\n".format(datetime.date.today(), temperature, e))

 error_file.close()
 log_file.close()
 counter = counter + 1 #testing to limit loops



# something like this for life func



while(true)

    timer

    while(timer > 60)
        something something darkside

    make 1 hour request
    reset timer