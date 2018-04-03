import cv2
import io
import argparse
import sys
import dlib
import json
import subprocess
import requests

from picamera import PiCamera
from picamera.array import PiRGBArray

robot_id = None
#server URL
URL = 'http://38.88.75.83/db/uploadfile2.php'
global_counter = 0

"""
    Starts infrared camera to detect faces and send a livestream to server.
    
"""
def start_camera():

    #Initialize camera 
    camera = PiCamera()
    stream = io.BytesIO()
    
    #Set camera resolution and framerate 
    camera.resolution =(608,480)
    camera.framerate = 50
    rawCapture = PiRGBArray(camera, size=(608,480))

    #Create HOG face detector from dlib class
    face_detector = dlib.get_frontal_face_detector()

    #Slows speed at which images are sent to server
    counter = 0
    global_counter = 0

    #Loop continuously for livestream
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
        frame = image.array
        
        #Convert image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rows, cols = gray.shape
        #Flip image upside down 
        MU = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)), 180, 1)
        grayup = cv2.warpAffine(gray,MU,(int(cols/2), int(rows/2)))
        
        #Rotate image left 90 degrees
        ML = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)),90, 1)
        grayleft = cv2.warpAffine(gray,ML,(int(cols/2), int(rows/2)))
        
        #Rotate image right 90 degrees
        MR = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)),270, 1)
        grayright = cv2.warpAffine(gray,MR,(int(cols/2), int(rows/2)))
        
        #Retrieve detected faces for rotated images
        detected_faces = face_detector(grayup,1)
        detected_left = face_detector(grayleft,1)
        detected_right = face_detector(grayright,1)
        
        
        #If faces are detected, crop images and send to server
        if (len(detected_faces) + len(detected_left) + len(detected_right) > 0):
            for i, face_rect in enumerate(detected_left):
            
                #Crop photo from rotated color image
                frameLeft = cv2.warpAffine(frame, MR,(int(cols/2), int(rows/2)))
                #Crop image to only detected face 
                crop = frameLeft[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]        
                name = "face" + str(global_counter) + ".jpg"
                #Save image
                cv2.imwrite(name, crop)
                image = {'photo':open(name, 'rb')}
                #Send to server 
                requests.post(URL, files = image)
                global_counter += 1

            for i, face_rect in enumerate(detected_right):
                #Crop photo from rotate color image
                frameRight = cv2.warpAffine(frame,MR,(int(cols/2), int(rows/2)))
                crop = frameRight[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
                name = "face" + str(global_counter) + ".jpg"
                #Save image 
                cv2.imwrite(name, crop)
                image = {'photo':open(name, 'rb')}
                #Send to server 
                requests.post(URL, files = image)
                global_counter += 1
                
            for i, face_rect in enumerate(detected_faces):
                #Crop photo from rotate colour image
                frameUp = cv2.warpAffine(frame, MU,(int(cols/2), int(rows/2)))
                crop = frameUp[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
                name = "face" + str(global_counter) + ".jpg"
                cv2.imwrite(name, crop)
                image = {'photo':open(name, 'rb')}
                requests.post(URL, files = image)
                #Increment face counter
                global_counter += 1
        
        #Update livestream 
        if (counter == 2):
            cv2.imwrite("frame.jpg", frame)
            image = {'photo':open('frame.jpg', 'rb')}
            requests.post(URL, files = image)
            counter = 0
        
        #Increment speed counter 
        counter += 1
        
        #Reset buffer
        stream.truncate()
        stream.seek(0)
        rawCapture.truncate(0)

# Function commands/help/options
def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-help",action= "help", default=argparse.SUPPRESS, 
                        help = "Start camera livestream and face detection.")
    
    args = parser.parse_args()
    start_camera();

if __name__ == '__main__':
   main()
