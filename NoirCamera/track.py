import cv2
import numpy as np
import argparse

buff_attr             = (20,20)
SEARCH_THRES          = 0.96
large_move_x          = 250
large_move_y          = 250
sw_y                  = 25
sw_x                  = 25
MATCH_METHOD          = 3
THICKNESS             = 1
blue                  = (255,0,0)
green                 = (0,255,0)
red                   = (0,0,255)
sw_w                  = 0
sw_h                  = 0
sx_y                  = 0
sx_x                  = 0
sw_xy                 = 0
font                  = cv2.FONT_HERSHEY_SIMPLEX
topLeft               = (200,25)
fontScale             = 0.5
fontColor             = (255,255,255)
lineType              = 2


"""
Tracks camera movement. 

@param v: verbose?
"""
def track(v):
    video_cap = cv2.VideoCapture(0) #image from video (default webcam)
    
    width = int (video_cap.get(3))
    height = int (video_cap.get(4))
    
    
    sw_w = width/4 #width/4
    sw_h = height/4 #height/4
    
    sw_x = int(width/2 - sw_w/2)
    sw_y = int(height/2 - sw_h/2)
    
    #Buffer size
    buff_attr = (int(sw_w/4), int(sw_h/4))
    
    sw_xy = (int (sw_w), int (sw_y))
    
    #Initial box location
    xy = (width/2, height/2)
    
    #Variables to track number of times out of frame
    WIDTH_TOTAL           = 0
    HEIGHT_TOTAL          = 0
    
    ret, frame = video_cap.read()
    
    #Create new search image 
    search_box = frame[sw_y: sw_y + sw_h, sw_x: sw_x + sw_w]
    
    #Display initial search image captured in red
    cv2.rectangle(frame, (sw_x, sw_y),
                         (sw_x + sw_w, sw_y + sw_h),
                          red, THICKNESS)
                          
    #Tracks previous and current coordinates of image location 
    new_coord = sw_xy
    prev_coord = new_coord
    reset = False;
    
    cv2.imshow('Video', frame)
    
    while True:
    #capture frame by frame
    #returns return code(tells us if we have run out of frames)
    #frame = one frame
        ret, frame = video_cap.read()
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert to grayscale 
        
        #return most probable location of search image in current frame
        new_coord, xy_val, min_loc, min_val = check_match(frame, search_box) 
        
        #Display intiial search image captured in red
        cv2.rectangle(frame, (sw_x, sw_y),
                     (sw_x + sw_w, sw_y + sw_h),
                      red, THICKNESS)
                      
        cv2.putText(frame, "Out of Frames W:{} H:{}".format(WIDTH_TOTAL, HEIGHT_TOTAL), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, blue, 2)   
                
        #if prev_coord differs from new_coord, but not by large_move amount, 
        #increase width or height total variables.
       
        if moved (prev_coord, new_coord): 
        
            #If too large of a move or if the search image cannot be found, reset image
            if (large_move(prev_coord, new_coord) or
                low(xy_val)):
                reset = True
            if (out_of_bounds_width(new_coord, video_cap, width)):
                reset = True
                WIDTH_TOTAL += 1    
            if (out_of_bounds_height(new_coord, video_cap, height)):
                reset = True
                HEIGHT_TOTAL += 1   
                
            #If image is still within bounds, display location of moved image as blue box
            else:
                xy = update_pos(xy, new_coord)
                prev_coord = new_coord
                cv2.rectangle(frame, (xy[0], xy[1]),
                         (xy[0] + sw_w, xy[1] + sw_h),
                          blue, THICKNESS*3)
        
        #If needs reset, find new search image
        if reset:
            ret, frame = video_cap.read()
            search_box = frame[sw_y: sw_y + sw_h, sw_x: sw_x + sw_w]
            new_coord = sw_xy
            prev_coord = new_coord
            reset = False
            xy = update_pos(xy, new_coord)
            if (v):
                cv2.rectangle(frame, (new_coord[0], new_coord[1]),
                             (new_coord[0] + sw_w, new_coord[1] + sw_h),
                              green, THICKNESS)
                         
        cv2.imshow('Video', frame)
        
        # Close when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_cap.release()
    cv2.destroyAllWindows()

"""
Check for match of search image in frame capture 

@param frame: frame image
@param image: search image 
"""    
def check_match(frame, image):
    #Searches for match in frame with original image
    result = cv2.matchTemplate(frame, image, MATCH_METHOD)
    #(x,y) of best and worst image match
    min_Val, max_Val, min_Loc, max_Loc = cv2.minMaxLoc(result)
    return max_Loc, max_Val, min_Loc, min_Val


"""
Checks if search image is now out of bounds vertically.

@param coord: current x, y coordinates
@param video_cap: video 
@param height
"""    
def out_of_bounds_height(coord, video_cap, height):
    return (coord[1] > (height - (buff_attr[1] + sw_h)) or
        coord[1] < buff_attr[1])

"""
Checks if search image is now out of bounds horiziontally.

@param coord: current x, y coordinates
@param video_cap: video 
@param width
"""   
def out_of_bounds_width(coord, video_cap, width):
    return (coord[0] > (width - (buff_attr[0] + sw_w)) or 
        coord[0] < buff_attr[0])
"""
Check if search image has moved in frame 

@param prev_coord: previous xy coordinates of search image 
@param coord: current xy coordinates of search image 
"""    
def moved(prev_coord, coord):
    return (int(coord[0]) != int(prev_coord[0]) or
            int(coord[1]) != int(prev_coord[1]))

"""
Check if search image is no longer in frame

@param xy_val: probability of search image in frame
"""            
def low(xy_val):
    return xy_val < SEARCH_THRES

"""
Check if search image has suddenly moved a lot

@param prev_coord: previous xy coordinates of search image 
@param coord: current xy coordinates of search image 
"""     
def large_move(prev_coord, new_coord):
    return((abs(new_coord[0] - prev_coord[0]) > large_move_x) or
            (abs(new_coord[1] - prev_coord[1]) > large_move_y))

"""
Update current position of search image 

@param prev_coord: previous xy coordinates of search image 
@param coord: current xy coordinates of search image 
"""              
def update_pos(xy, new_coord):
    xy = (new_coord[0], new_coord[1])
    return xy
 
# Function commands/help/options
def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "-help",action= "help", default=argparse.SUPPRESS, 
                        help = "Function uses OpenCV's template matching to track camera/robot movement.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    
    args = parser.parse_args()
    track(args.verbose)

if __name__ == '__main__':
   main()