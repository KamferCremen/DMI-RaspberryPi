import smbus
import time
import RPi.GPIO as GPIO

bus = smbus.SMBus(1)
bus.write_byte(0x48, 0x00)

while(True):

 measure = bus.read_byte(0x48)

 while(measure > 200):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(18, GPIO.OUT)
  measure = bus.read_byte(0x48)
  GPIO.output(18, GPIO.HIGH)
  print(measure)
  time.sleep(2)

 GPIO.setmode(GPIO.BCM)
 GPIO.setup(18, GPIO.OUT)
 GPIO.output(18, GPIO.LOW)
 print(measure)
 GPIO.cleanup()

 time.sleep(2)
