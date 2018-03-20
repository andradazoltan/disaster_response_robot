import cv2
import numpy as np
import argparse

box_attr              = (100,100)
buff_attr             = (20,20)
SEARCH_THRES          = 0.96
box_h                 = 100
box_w                 = 100
large_move_x          = 30
large_move_y          = 30
sw_y                  = 25
sw_x                  = 25
MATCH_METHOD          = 3
THICKNESS             = 1
green                 = (255,0,0)
sw_w                  = 0
sw_h                  = 0
sx_y                  = 0
sx_x                  = 0
sw_xy                 = 0

def track(v):
    video_cap = cv2.VideoCapture(0) #image from video (default webcam)
    
    sw_w = int(video_cap.get(3)/4) #width/4
    sw_h = int(video_cap.get(4)/4) #height/4
    
    sw_x = int(int(video_cap.get(3)/2) - sw_w/2)
    sw_y = int(int(video_cap.get(4)/2) - sw_h/2)
    
    buff_attr = (int(sw_w/4), int(sw_h/4))
    
    sw_xy = (int (sw_w), int (sw_y))
    
    xy = (0,0)
    ret, frame = video_cap.read()
    
    #Create new search image 
    search_box = frame[sw_y: sw_y + box_h, sw_x: sw_x + box_w]
    new_coord = sw_xy
    prev_coord = new_coord
    
    
    while True:
        ret, frame = video_cap.read()
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        new_coord, xy_val = check_match(frame, search_box)
        
        if moved (prev_coord, new_coord): 
            if (large_move(prev_coord, new_coord) or
                out_of_bounds(new_coord, video_cap) or low(xy_val)):
                reset = True
            else:
                xy = update_pos(xy, prev_coord, new_coord)
                prev_coord = new_coord
                cv2.rectangle(frame, (xy[0], xy[1]),
                         (xy[0] + sw_w, xy[1] + sw_h),
                          green, THICKNESS)
        
        if reset:
            search_box = frame[sw_y: sw_y + box_h, sw_x: sw_x + box_w]
            new_coord = sw_xy
            prev_coord = new_coord
            
            cv2.rectangle(frame, (new_coord[0], new_coord[1]),
                         (new_coord[0] + sw_w, new_coord[1] + sw_h),
                          green, THICKNESS)
                         
        cv2.imshow('Video', frame)
        
        # Close when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_cap.release()
    cv2.destroyAllWindows()
    
def check_match(frame, image):
    #Searches for match in frame with original image
    result = cv2.matchTemplate(frame, image, MATCH_METHOD)
    #(x,y) of best and worst image match
    min_Val, max_Val, min_Loc, max_Loc = cv2.minMaxLoc(result)
    return max_Loc, max_Val
    
def out_of_bounds(coord, video_cap):
    width = video_cap.get(3)
    height = video_cap.get(4)
    
    if (coord[0] > (width - (buff_attr[0] + sw_w)) or 
        coord[0] < buff_attr[0] or
        coord[1] > (height - (buff_attr[1] + sw_h)) or
        coord[1] < buff_attr[1]):
        return True
    else: return False
    
   
def moved(prev_coord, coord):
    return (int(coord[0]) != int(prev_coord[0]) or
            int(coord[1]) != int(prev_coord[1]))
            
def low(xy_val):
    return xy_val < SEARCH_THRES
    
def large_move(prev_coord, new_coord):
    return((abs(new_coord[0] - prev_coord[0]) > large_move_x) or
            (abs(new_coord[1] - prev_coord[1]) > large_move_y))
            
def update_pos(xy, prev_coord, new_coord):
    dx = 0
    dy = 0
    if (abs(prev_coord[0] - new_coord[0]) > 0):
        dx = prev_coord[0] - new_coord[0] 
    if (abs(prev_coord[1] - new_coord[1]) > 0):
        dy = prev_coord[1] - new_coord[1] 
    xy = (xy[0] + dx, xy[1] + dy)
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