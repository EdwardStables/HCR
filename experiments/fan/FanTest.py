import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
print("FAN ON")
GPIO.output(18, GPIO.HIGH)
time.sleep(10)
print("FAN OFF")
GPIO.output(18, GPIO.LOW)
