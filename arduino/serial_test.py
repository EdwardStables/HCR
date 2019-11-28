from time import sleep
import serial
ser = serial.Serial('COM3', 9600) # Establish the connection on a specific port#
serial_command = ""
data_available = False

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

while True:
     command = input("Enter command: ")
     data = command.split()
     if data[0] == "pattern":
          serial_command = "{\"instr\":1,\"pattern\":"\
                              + data[1] + "}"
     elif data[0] == "move":
          serial_command = "{\"instr\":2,\"move\":["\
                              + data[1] + ","\
                              + data[2] + ","\
                              + data[3] + ","\
                              + data[4] + ","\
                              + data[5] + ","\
                              + data[6] + "]}"
     elif data[0] == "offset": 
          serial_command = "{\"instr\":3,\"offset\":["\
                              + data[1] + ","\
                              + data[2] + "]}"
     elif data[0] == "colour":
          serial_command = "{\"instr\":4,\"colour\":\""\
                              + data[1] + "\"}"
     else: 
          serial_command = "{\"instr\":0}"

     ser.write(serial_command.encode())
     ser.flush()
     sleep(1)
     while ser.inWaiting():
          print(ser.readline())