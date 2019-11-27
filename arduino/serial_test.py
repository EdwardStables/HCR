from time import sleep
import serial
ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port#
string = "{\"instr\":1,\"pattern\":0}"
print("pre-send")
ser.write(string.encode())
print("post-send")
while True:
     print(ser.readline()) # Read the newest output from the Arduino
