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
URL = 'http://38.88.75.83/db/uploadfile2.php'
global_counter = 0

def start_camera():

    camera = PiCamera()
    stream = io.BytesIO()
    camera.resolution =(608,480)
    camera.framerate = 50
    rawCapture = PiRGBArray(camera, size=(608,480))

    #Create HOG face detector from dlib class
    face_detector = dlib.get_frontal_face_detector()
    #landmark_predictor_model = "shape_predictor_68_face_landmarks.dat"

    counter = 0
    global_counter = 0

    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
        frame = image.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rows, cols = gray.shape
        MU = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)), 180, 1)
        grayup = cv2.warpAffine(gray,MU,(int(cols/2), int(rows/2)))
        ML = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)),90, 1)
        grayleft = cv2.warpAffine(gray,ML,(int(cols/2), int(rows/2)))
        MR = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)),270, 1)
        grayright = cv2.warpAffine(gray,MR,(int(cols/2), int(rows/2)))
        detected_faces = face_detector(grayup,1)
        detected_left = face_detector(grayleft,1)
        detected_right = face_detector(grayright,1)
        
    
        if (len(detected_faces) + len(detected_left) + len(detected_right) > 0):
            for i, face_rect in enumerate(detected_left):
                frameLeft = cv2.warpAffine(frame, MR,(int(cols/2), int(rows/2)))
                crop = frameLeft[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]        
                name = "face" + str(global_counter) + ".jpg"
                print(name)
                cv2.imwrite(name, crop)
                image = {'photo':open(name, 'rb')}
                #requests.post(URL, files = image)
                global_counter += 1

            for i, face_rect in enumerate(detected_right):
                frameRight = cv2.warpAffine(frame,MR,(int(cols/2), int(rows/2)))
                crop = frameRight[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
                
                name = "face" + str(global_counter) + ".jpg"
                cv2.imwrite(name, crop)
                print(name)
                image = {'photo':open(name, 'rb')}
                #requests.post(URL, files = image)
                global_counter += 1
                
            for i, face_rect in enumerate(detected_faces):
                frameUp = cv2.warpAffine(frame, MU,(int(cols/2), int(rows/2)))
                crop = frameUp[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
                name = "face" + str(global_counter) + ".jpg"
                cv2.imwrite(name, crop)
                print(name)
                image = {'photo':open(name, 'rb')}
                #requests.post(URL, files = image)
                global_counter += 1
                
        if (counter == 2):
            cv2.imwrite("frame.jpg", frame)
            image = {'photo':open('frame.jpg', 'rb')}
            #requests.post(URL, files = image)
            counter = 0
            
        print(counter)
        counter += 1
        
        stream.truncate()
        stream.seek(0)
        rawCapture.truncate(0)

# Function commands/help/options
def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-help",action= "help", default=argparse.SUPPRESS, 
                        help = "Function uses OpenCV's template matching to track camera/robot movement.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    
    args = parser.parse_args()
    start_camera();

if __name__ == '__main__':
   main()
