# Main function for face detection/recognition
# Function options:
#   - Display 68 facial "landmarks"
#   - Saves found faces through webcam as jpg
#   - ...movement of mouth?
#   - compare characteristics to given image 
# Currently testing using webcam before using RPi Noir (part not yet arrived :()

import cv2
import sys
import dlib 
import argparse
import imutils
import numpy as np
from scipy.spatial import distance 
import math
import time 

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

    #Create HOG face detector from dlib class
    face_detector = dlib.get_frontal_face_detector()
    landmark_predictor_model = "shape_predictor_68_face_landmarks.dat"
    face_pose_predictor = dlib.shape_predictor(landmark_predictor_model)

    video_cap = cv2.VideoCapture(0) #image from video (default webcam)
    
    #if no one is in the frame
    last = True
    (leftStart, leftEnd) = facial_locations["left_eye"]
    (rightStart, rightEnd) = facial_locations["right_eye"]

    
    EYE_THRESH             = 0.3
    EYE_FRAMES             = 3
    COUNTER                = 0
    TOTAL                  = 0

    while True:
    #capture frame by frame
    #returns return code(tells us if we have run out of frames)
    #frame = one frame
        ret, frame = video_cap.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        detected_faces = face_detector(gray, 1)
        
        if (v): print("Found {} faces in this frame.".format(len(detected_faces)))
        
        if (len(detected_faces) == 0): last = True
        
        
        # Loop through all faces found
        for i, face_rect in enumerate(detected_faces):
            if (v): print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))

            # Draw a box around each face we found
            cv2.rectangle(frame, (face_rect.left(), face_rect.top()), (face_rect.right(), face_rect.bottom()), 
                            (0, 255, 0), 2)
            crop = frame[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
            
                
            #Generate and store landmarks 
            face_landmarks = face_pose_predictor(frame, face_rect)
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
            
        cv2.imshow('Video', frame)
            
        
        # Close when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_cap.release()
    cv2.destroyAllWindows()

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
Converts landmarks into array of tuples with (x,y)

@param frame: face_landmarks
@return points array withs (x,y) tuples
"""    
def store_landmarks(face_landmarks):
    points = np.zeros((68,2), dtype=int)
    
    for i in range (0,68):
        points[i] = (face_landmarks.part(i).x, face_landmarks.part(i).y)
    return points 
    
"""
Determines if characteristics in face found are similar to image

@param f: name of file with given image to compare to
@param image : face found through webcam
"""    
def compare_to_image(f, image):
    return 

        
# Function commands/help/options
def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-help",action= "help", default=argparse.SUPPRESS, 
                        help = "Function identifies faces found with webcam; will locate 68 landmarks and bounding box.")
    parser.add_argument("-l", "--landmarks", help = "Show found landmarks when face found.", action="store_true")
    parser.add_argument("-s", "-save", help = "Saves images of faces detected through webcam as jpg.", type=bool,required =False)
    parser.add_argument("-f", "-file", help = "Add image to determine likelihood given face is seen through webcam.", type=str, required=False)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-a", "--alive", help="is this person alive (detect movement)", action="store_true")
    
    args = parser.parse_args()
    findFace(args.landmarks, args.s, args.f, args.verbose, args.alive)

if __name__ == '__main__':
   main()