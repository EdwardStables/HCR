#!/usr/bin/env python
import cv2
import sys
from os import path
import time

root = "/home/ed/Documents/code/python/open_cv_test/"
cascPath = path.join(root, "util_file/haarcascade_frontalface_default.xml")
faceCascade = cv2.CascadeClassifier(cascPath)
font = cv2.FONT_HERSHEY_SIMPLEX

video_capture = cv2.VideoCapture(4)
#video_capture = cv2.VideoCapture(path.join(root, 'util_file/mock_the_week.mp4'))

while True:
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    cv2.putText(frame, "Faces: {}".format(len(faces)), (0,frame.shape[0]), font, 4, (255,255,255), 2, cv2.LINE_AA)
    cv2.imshow('Video', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
