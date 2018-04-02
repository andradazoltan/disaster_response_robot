import cv2
import sys
import dlib 
import argparse
import imutils
import numpy as np
from scipy.spatial import distance 
import math
import time
import json
import subprocess
import requests

from picamera import PiCamera
from picamera.array import PiRGBArray

URL = 'http://38.88.75.83/db/uploadfile2.php'

def start_camera():
    camera = PiCamera()
    stream = io.BytesIO()
    camera.resolution = (128,128)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(128,128))

    #Create HOG face detector from dlib class
    face_detector = dlib.get_frontal_face_detector()
    landmark_predictor_model = "shape_predictor_68_face_landmarks.dat"

    counter = 0

    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
        frame = image.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rows, cols = gray.shape
        ML = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)),90, 1)
        grayleft = cv2.warpAffine(gray,ML,(int(cols/2), int(rows/2)))
        MR = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)),270, 1)
        grayright = cv2.warpAffine(gray,MR,(int(cols/2), int(rows/2)))
        detected_faces = face_detector(gray,1)
        detected_left = face_detector(grayleft,1)
        detected_right = face_detector(grayright,1)
    
        #if (len(detected_faces) + len(detected_left) + len(detected_right) > 0): #face detected
        
        if (counter == 90):
            requests.post(URL, files = frame)
            counter = 0
        counter += 1
            
        #crop = frame[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]

    stream.truncate()
    stream.seek(0)
    rawCapture.truncate(0)
