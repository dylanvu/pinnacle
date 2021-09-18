import cv2
import time
import numpy as np

from picamera.array import PiRGBArray
from picamera import PiCamera

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
cameraMatrix = np.genfromtxt("/home/pi/Documents/pinnacle/calibration/camera_matrix.txt")
dist = np.genfromtxt("/home/pi/Documents/pinnacle/calibration/distortion.txt")

ret,frame = cap.read() # return a single frame in variable `frame`
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
h,w = frame.shape[:2]
newCameraMatrix, roi = cv2. getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h),1, (w,h))


while(True):
    ret,frame = cap.read() # return a single frame in variable `frame`
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     h,w = frame.shape[:2]
#     newCameraMatrix, roi = cv2. getOpt
    ust = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)

#     cv2.imshow('Capturing Video',ust) #display the captured image
    x, y, w, h = roi
    ust = ust[y:y+h, x:x+w]
    
    cv2.imshow('Capturing Video',ust) #display the captured image

    key = cv2.waitKey(1) & 0xFF
    if key == ord('y'): # exit on pressing 'y' 
        cv2.destroyAllWindows()
        break


cap.release()
