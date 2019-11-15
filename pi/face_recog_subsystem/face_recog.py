import cv2 as cv
import sys, time
from os import path 
from time import time, sleep
from collections import deque

from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody


class face_recog(subsystem):
    """Detects faces in camera feed. Detects a subscriber request 
    from other subsystems and sends updates with the requested frequency.
    """


    def __init__(self, root_path, video_capture_num, pos_sub=[], num_sub=[], rel_sub=[]):
        """Root path required for openCV pathing to work.
        Default subscribers are subscribers that want to always get faces.
        Each subscriber should be in the format (str, bool) where the string
        gives ID, and the bool denotes if full position is desired, otherwise
        only the number of people present is returned. 
        video_capture_number is the camera number.
        """
        self.root = path.join(root_path, 'face_recog_subsystem')
        self.video_capture_num = video_capture_num
        cascPath = path.join(self.root, 'haarcascade_frontalface_default.xml')
        self.faceCascade = cv.CascadeClassifier(cascPath)
        self.video_capture = cv.VideoCapture(self.video_capture_num)

        self.width = self.video_capture.get(3)
        self.height = self.video_capture.get(4)

        self.relative_face_buffer= deque(maxlen=5)

        self.position_subscribers = pos_sub
        self.number_subscribers = num_sub
        self.relative_subscribers = rel_sub
        super().__init__("face_recog", "id_only")

    def _run(self):
        self.scan_time = 0.01 
        self.t1 = time()
        self.message_check_countdown = 10
        self.status = "Main Loop"
        self.main_loop()

    def subsys_update(self):
        """Perform updates for the subsystem in the mainloop"""

        if self.message_check_countdown == 0:
            self.check_messages()
            self.message_check_countdown = 10
        else:
            self.message_check_countdown -= 1

        #slp = self.scan_time - (time() - self.t1)
        #if slp > 0:
        #    sleep(slp)
        self.t1 = time()
        
    def main_loop(self):
        while True:
            self.subsys_update()

            ret, frame = self.video_capture.read()
            
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30,30),
                flags=cv.CASCADE_SCALE_IMAGE
            )

            self.send_faces(faces)

    def send_faces(self, faces):
        num_faces = len(faces)
        for s in self.number_subscribers:
            self.send_message(s, "num_faces", num_faces)

        for s in self.position_subscribers:
            self.send_message(s, "pos_faces", faces)

        if num_faces:
            relative_faces = self.calculate_relative_faces(faces)
            for s in self.relative_subscribers:
                self.send_message(s, "rel_faces", relative_faces)

    def calculate_relative_faces(self, faces):
        face = max(faces, key=lambda f: (f[2]-f[0])*(f[3]-f[1]))

        x=face[0] + (face[2]/2)
        y=face[1] + (face[3]/2)
        x = -1 * round(2*x/self.width - 1, 3)
        y = round(-2*y/self.height + 1, 3)

        self.relative_face_buffer.append((x,y))

        return self.get_buffer_average()

    def get_buffer_average(self):
        x = 0
        y = 0
        for f in self.relative_face_buffer:
            x += f[0]
            y += f[1]
        return (x/len(self.relative_face_buffer),
                y/len(self.relative_face_buffer))

    def check_messages(self):
        messages = self.get_messages()
        for m in messages:
            #Subscriber updates
            if m.ref == "pos_subscribe":
                self.position_subscribers.append(m.sender_id)
            elif m.ref == "pos_unsubscribe" and m.sender_id in self.position_subscribers:
                self.position_subscribers.remove(m.sender_id)
            elif m.ref == "num_subscribe":
                self.number_subscribers.append(m.sender_id)
            elif m.ref == "num_unsubscribe" and m.sender_id in self.number_subscribers:
                self.number_subscribers.remove(m.sender_id)
            elif m.ref == "rel_subscribe":
                self.relative_subscribers.append(m.sender_id)
            elif m.ref == "rel_unsubscribe" and m.sender_id in self.relative_subscribers:
                self.relative_subscribers.remove(m.sender_id)

            #Internal Data
            elif m.ref == "get_subscribers":
                self.send_message(m.sender_id, 
                                  "get_subscribers_reply",
                                  {"position" : self.position_subscribers,
                                   "number"   : self.number_subscribers,
                                   "relative" : self.relative_subscribers},
                                 )

