import cv2
import time
from centroidScript import *

def CalibrateDot(cap, frame, cameraMatrix, dist, newCameraMatrix, roi):
    ret,frame = cap.read() # return a single frame in variable `frame`
    ust = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix) # undistort
    # Get final frame to process
    x, y, w, h = roi
    ust = ust[y:y+h, x:x+w]
    ((cX,cY), color) = centroidScript(ust)
    time.sleep(0.5)
    return (cX, cY)