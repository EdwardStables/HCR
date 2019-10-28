import cv2 as cv

from os import path 
import sys, time

root = "/home/ed/Documents/university/year4/human_centered_robotics/HCR_2019/experiments/opencv_headless"
cascPath = path.join(root, 'haarcascade_frontalface_default.xml')
faceCascade = cv.CascadeClassifier(cascPath)

video_capture = cv.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30),
        flags=cv.CASCADE_SCALE_IMAGE
    )
    x_big = ybig = 0
    area_max = 0
    if len(faces) == 1:
        x_big = faces[0][0]
        y_big = faces[0][1]
    else:
        for x,y,w,h in faces:
            new_area = w * h
            if new_area > area_max:
                x_big = x
                y_big = y
                area_max = new_area
    
    
    print(x_big, y_big)

video_capture.release()