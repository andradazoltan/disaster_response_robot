# Main function for face detection/recognition
# Function options:
#   - Add image; displays text if the image "matches" face found in webcam
#   - Display 68 facial "landmarks"
#   - Saves found faces through webcam as jpg
# Currently testing using webcam before using RPi Noir (part not yet arrived :()

import cv2
import sys
import dlib 
import argparse

"""
Finds face with webcam

@param arg.l: include landmarks?
@param arg.s: save faces found?
@param arg.f: compare with given face?
"""
def findFace(arg.l, arg.s, args.f):

    #Create HOG face detector from dlib class
    face_detector = dlib.get_frontal_face_detector()
    landmark_predictor_model = "shape_predictor_68_face_landmarks.dat"
    face_pose_predictor = dlib.shape_predictor(landmark_predictor_model)

    video_cap = cv2.VideoCapture(0) #image from video (default webcam)
    
    while True:
    #capture frame by frame
    #returns return code(tells us if we have run out of frames)
    #frame = one frame
        ret, frame = video_cap.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        detected_faces = face_detector(gray, 1)
        
        print("Found {} faces in this frame.".format(len(detected_faces)))
        
        # Loop through all faces found
        for i, face_rect in enumerate(detected_faces):
            print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))

            # Draw a box around each face we found
            cv2.rectangle(frame, (face_rect.left(), face_rect.top()), (face_rect.right(), face_rect.bottom()), 
                            (0, 255, 0), 2)
            crop = frame[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
            if (arg.s):
                cv2.imwrite("crop.jpg", crop)
                
            if (arg.l):
                face_landmarks = face_pose_predictor(frame, face_rect)
                frame = show_landmarks(frame, face_landmarks)
        
        
        #cv2.putText(frame, "FIND DA FACE".format(alpha),
        #    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
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
def show_landmarks(frame, face_landmarks):
    frame = frame.copy()
    for i, point in enumerate(face_landmarks):
        pos = (point[0, 0], point[0, 1])
        cv2.putText(frame, str(i), pos,
                    fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    fontScale=0.4,
                    color=(0, 0, 255))
        cv2.circle(im, pos, 3, color=(0, 255, 255))
    return frame
    
"""
Determines if face "matches" face found in given image

@param fileName: name of file with given image to compare to
@param ... : face found through webcam
"""    
def compare_to_image(args.f):

        
# Function commands/help/options
def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-help",action= "help", default=argparse.SUPPRESS, 
                        help = "Function identifies faces found with webcam; will locate 68 landmarks and bounding box.")
    parser.add_argument("-l", "-landmarks", help = "Add filename with data to be parsed and graphed.", type=bool, required=False)
    parser.add_argument("-s", "-save", help = "Saves images of faces detected through webcam as jpg.", type=bool,required =False)
    parser.add_argument("-f", "-file", help = "Add image to determine likelihood given face is seen through webcam.", type=str, required=false)
    args = parser.parse_args()
    findFace(args.l, args.s, args.f)

if __name__ == '__main__':
   main()