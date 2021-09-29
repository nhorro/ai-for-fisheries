import sys
sys.path.append("../videoanalytics/src")
import videoanalytics
import cv2
import numpy as np

from datetime import datetime


def add_point_to_roi(event,x,y,flags,param):
    global g_mouse_x, g_mouse_y
    g_mouse_x,g_mouse_y = x,y

if __name__ == "__main__":
    global g_mouse_x, g_mouse_y
    g_mouse_x = 0
    g_mouse_y = 0

    roi_points = []
    
    INPUT_VIDEO = "../data/media/fishcount/input_videos/003.mp4"
    
    
    cap = cv2.VideoCapture(INPUT_VIDEO)

    if (cap.isOpened()== False):
        print("Error opening video stream or file")
    print("Q to quit")

    cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('Frame',add_point_to_roi)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:

            for roi in roi_points:
                cv2.circle(frame,(roi[0],roi[1]),5,(255,0,0),-1) 
            
            cv2.imshow('Frame',frame)        
            pressed_key = cv2.waitKey(25) & 0xFF
            if pressed_key == ord('q'):
                break
            elif pressed_key == ord('a'):
                print(g_mouse_x,g_mouse_y)
                roi_points.append((g_mouse_x,g_mouse_y))
        else:
            break
    
    cap.release()
    cv2.destroyAllWindows()