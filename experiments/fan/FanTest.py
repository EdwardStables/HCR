import RPi.GPIO as GPIO
from time import sleep
import subprocess
import sys

ON_TEMP = 60
OFF_TEMP = 55
FAN_PIN = 12 

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(FAN_PIN, GPIO.OUT)

def poll():
    val = subprocess.getoutput("vcgencmd measure_temp")#, shell=True)
    val = val.split('=')[-1]
    val = val.split("'")[0]
    return float(val)
    
def fan_on():
    GPIO.output(FAN_PIN, GPIO.HIGH)

def fan_off():
    GPIO.output(FAN_PIN, GPIO.LOW)

def main_loop(PRINT):
    while True:

        temp = poll()

        if PRINT:
            print(temp)

        if temp > ON_TEMP:
            fan_on()
        elif temp < OFF_TEMP:
            fan_off()

        sleep(1)

def argparse(arg):

    if len(arg) > 1 and "print" ==  arg[1]:
        return True
    else:
        return False
    

if __name__ == "__main__":
    setup()
    PRINT = argparse(sys.argv)
    main_loop(PRINT)
