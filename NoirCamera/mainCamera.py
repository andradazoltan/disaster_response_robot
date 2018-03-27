# Main function for face detection/recognition

from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import io
import argparse
import imutils
from scipy import ndimage
import sys
import math
import dlib
import numpy as np
from scipy.spatial import distance 

font                   = cv2.FONT_HERSHEY_SIMPLEX
topLeft                = (200,25)
fontScale              = 0.5
fontColor              = (255,255,255)
lineType               = 2

facial_locations = {"mouth": (48,68), "right_eyebrow": (17,22),
                    "left_eyebrow": (22, 27), "right_eyebrow":(36, 42),
                    "right_eye": (36, 42), "left_eye": (42, 48),
                    "nose": (27, 35), "jaw": (0,17)}    


"""
Finds face with webcam

@param l: include landmarks?
@param s: save faces found?
@param f: compare with given face?
@param v: verbose?
"""
def findFace(l, s, f, v, a):

    camera = PiCamera()
    stream = io.BytesIO()
    camera.resolution = (128,128)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(128,128))

    #Create HOG face detector from dlib class
    face_detector = dlib.get_frontal_face_detector()
    landmark_predictor_model = "shape_predictor_68_face_landmarks.dat"
    face_pose_predictor = dlib.shape_predictor(landmark_predictor_model)
    
    #if no one is in the frame
    last = True
    (leftStart, leftEnd) = facial_locations["left_eye"]
    (rightStart, rightEnd) = facial_locations["right_eye"]
    (mouthStart, mouthEnd) = facial_locations["mouth"]
    prev_open = 0
    
    EYE_THRESH             = 0.3
    EYE_FRAMES             = 3
    MOUTH_MOVEMENT         = 0
    COUNTER                = 0
    TOTAL                  = 0

    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):

        frame = image.array
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("upright.jpg", gray)
        rows, cols = gray.shape
        ML = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)),90, 1)
        grayleft = cv2.warpAffine(gray,ML,(int(cols/2), int(rows/2)))
        cv2.imwrite("left.jpg", grayleft)
        MR = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)),270, 1)
        grayright = cv2.warpAffine(gray,MR,(int(cols/2), int(rows/2)))
        cv2.imwrite("right.jpg", grayright)
        detected_faces = face_detector(gray,1)
        detected_left = face_detector(grayleft,1)
        detected_right = face_detector(grayright,1)
        
        if (v): print("Found {} faces in this frame.".format(len(detected_faces) + len(detected_left) + len(detected_right)))
        
        if (len(detected_faces) + len(detected_left) + len(detected_right) == 0): last = True

        print(len(detected_left) + len(detected_right) + len(detected_faces))

        # Loop through all faces found
        for i, face_rect in enumerate(detected_faces):
            if (v): print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))

            # Draw a box around each face we found
            cv2.rectangle(frame, (face_rect.left(), face_rect.top()), (face_rect.right(), face_rect.bottom()), 
                            (0, 255, 0), 2)
            
            crop = frame[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]

            if (l):
                #Generate and store landmarks 
                face_landmarks = face_pose_predictor(gray, face_rect)
                points = store_landmarks(face_landmarks)
            
            if (a):
            #Collect facial feature coordinates
                leftEye = points[leftStart:leftEnd]
                rightEye = points[rightStart:rightEnd]
                lear = eye_aspect_ratio(leftEye)
                rear = eye_aspect_ratio(rightEye)
                aear = (lear + rear) / 2.0
                
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                
                if aear < EYE_THRESH: COUNTER += 1
                else: 
                    if COUNTER >= EYE_FRAMES: TOTAL += 1
                    COUNTER = 0
                
                
                cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)    

                mouth = points[mouthStart:mouthEnd]
                open = mouth_movement(mouth)
                if (open/prev_open > MOUTH_THRES and prev_open > 0):
                    MOUTH_MOVEMENT++
                    prev_open = open

            #If user wants to save faces, save into file
            #TODO: given filename save
            if (s and last):
                last = False
                cv2.imwrite("face.jpg", crop)
                
            
            #If user wants to show landmarks on screen
            if (l):
                frame = show_landmarks(frame, face_landmarks, points, v)

        # Loop through all faces found
        for i, face_rect in enumerate(detected_left):
            if (v): print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))

            # Draw a box around each face we found
            cv2.rectangle(frame, (face_rect.left(), face_rect.top()), (face_rect.right(), face_rect.bottom()), 
                            (0, 255, 0), 2)
            
            frameLeft = cv2.warpAffine(frame,MR,(int(cols/2), int(rows/2)))
            crop = frame[face_rect.left():face_rect.right(), face_rect.top():face_rect.bottom()]

            if (l):
                #Generate and store landmarks 
                face_landmarks = face_pose_predictor(gray, face_rect)
                points = store_landmarks(face_landmarks)
            
            if (a):
                #Collect facial feature coordinates
                leftEye = points[leftStart:leftEnd]
                rightEye = points[rightStart:rightEnd]
                lear = eye_aspect_ratio(leftEye)
                rear = eye_aspect_ratio(rightEye)
                aear = (lear + rear) / 2.0
                
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                
                if aear < EYE_THRESH: COUNTER += 1
                else: 
                    if COUNTER >= EYE_FRAMES: TOTAL += 1
                    COUNTER = 0
                              
                cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)    
                
            #If user wants to save faces, save into file
            #TODO: given filename save
            if (s and last):
                last = False
                cv2.imwrite("face.jpg", crop)
                
            
            #If user wants to show landmarks on screen
            if (l):
                frame = show_landmarks(frame, face_landmarks, points, v)
              
        #Display info 
        cv2.putText(frame,'SEARCHING FOR FACES...', 
            topLeft, 
            font, 
            fontScale,
            fontColor,
            lineType)        
            
        cv2.imshow('Frame', frame)
        stream.truncate()
        stream.seek(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        rawCapture.truncate(0)

"""
Overlays facial landmarks for given face over given frame.

@param frame: webcam captured frame
@param face_landmarks: location of landmarks for detected face
@return frame: original frame with landmarks overlayed ontop
"""        
def show_landmarks(frame, face_landmarks, points, v):

    frame = frame.copy()
    
    i = 1 #counter
    
    for (x,y) in points:
        pos = (x,y)
        
        if (v):
            cv2.putText(frame, str(i), pos,
                        fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                        fontScale=0.3,
                        color=(0, 0, 0))
        cv2.circle(frame, pos, 3, color=(0, 75, 255))
        
        i+=1
        
    return frame

"""
Formula from http://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf
Computes the euclidean distances between the two sets of eye landmarks with coordinates
(horizontal and vertical) to get eye aspect ratio.

@param eye: coordinates of given eye points 
@return ear: eye aspect ratio 
"""  
def eye_aspect_ratio(eye):

	a = distance.euclidean(eye[1], eye[5])
	b = distance.euclidean(eye[2], eye[4])
	c = distance.euclidean(eye[0], eye[3])
 
	# compute the eye aspect ratio
	ear = (a + b) / (2.0 * c)
 
	return ear
    
"""
Returns distance mouth edges.

@param mouth: coordinates of given mouth points
@return open: distance between top of mouth to bottom of center of mouth
"""
def mouth_movement(mouth):
    left = mouth[0]
    right = mouth [6]
    center_top = mouth[3]
    center_bottom = mouth[9]

    return distance.euclidean(center_top, center_bottom)

"""
Converts landmarks into array of tuples with (x,y)

@param frame: face_landmarks
@return points array withs (x,y) tuples
"""    
def store_landmarks(face_landmarks):
    points = np.zeros((68,2), dtype=int)
    for i in range (0,68):
        points[i] = (face_landmarks.part(i).x, face_landmarks.part(i).y)
    return points 

def testFrameRate():  
    camera = PiCamera()
    stream = io.BytesIO()
    camera.resolution = (800,608)
    camera.framerate = 80
    rawCapture = PiRGBArray(camera, size=(800,608))

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
        image = frame.array

        cv2.imshow("Frame", image)

        stream.truncate()
        stream.seek(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        rawCapture.truncate(0)
        
# Function commands/help/options
def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-help",action= "help", default=argparse.SUPPRESS, 
                        help = "Function identifies faces found with webcam; will locate 68 landmarks and bounding box.")
    parser.add_argument("-l", "--landmarks", help = "Show found landmarks when face found.", action="store_true")
    parser.add_argument("-s", "-save", help = "Saves images of faces detected through webcam as jpg.", action="store_true")
    parser.add_argument("-f", "-file", help = "Add image to determine likelihood given face is seen through webcam.", type=str, required=False)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-a", "--alive", help="is this person alive (detect movement)", action="store_true")
    
    args = parser.parse_args()
    findFace(args.landmarks, args.s, args.f, args.verbose, args.alive)
    #testFrameRate()

if __name__ == '__main__':
   main()
