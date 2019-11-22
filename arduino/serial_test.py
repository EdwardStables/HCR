from time import sleep
import serial
ser = serial.Serial('COM3', 9600) # Establish the connection on a specific port#
string = "{\"instr\":1,\"state\":0,\"moves\":[[0,0,40,0,0,0],[0,0,-30,0,0,0]]}"
ser.write(string.encode())
while True:
     print(ser.readline()) # Read the newest output from the Arduino