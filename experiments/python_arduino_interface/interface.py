import serial
from time import sleep

S = serial.Serial(port="/dev/ttyACM0", baudrate=9600)
sleep(1)
index = 0 
S.write(b"hello")
while True:
    data = S.readline()
    if data:
        print(data)