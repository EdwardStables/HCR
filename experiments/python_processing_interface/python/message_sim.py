import atexit
import json
import sockets
import time
"""
Message format for position:
message = {
    position : {
        posX : float,
        posY : float,
        posZ : float,
        rotX : float,
        rotY : float,
        rotZ : float
    }
}
"""

sender = sockets.connecter()

@atexit.register
def closer():
    sender.closer()

pos = [i/100 for i in range(-100, 100)]
index = 0
inc = 1

while True:
    sender.send("pos,{},0,0,0,0,0".format(pos[index]))
    index += inc
    if index in (len(pos)-1, 0):
        inc *= -1
    time.sleep(0.01)