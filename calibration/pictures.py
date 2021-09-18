import cv2
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

# camera = PiCamera()
# camSize = (640, 480)
# camera.resolution = camSize
# camera.framerate = 32

# rawCapture = PiRGBArray(camera, size=camSize)

# time.sleep(0.1)

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 

imgCount = 0 # Number of images

# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     ret,frame = cap.read() # return a single frame in variable `frame`
#     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('Capturing Video',frame) #display the captured image
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('y'): # exit on pressing 'y' 
#         cv2.destroyAllWindows()
#         break
#     if key == ord('c'): # save picture on pressing 'c' 
#         cv2.imwrite(str(imgCount) + ".jpg",frame)
#         imgCount += 1
#     rawCapture.truncate(0)


while(True):
    ret,frame = cap.read() # return a single frame in variable `frame`
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Capturing Video',frame) #display the captured image
    key = cv2.waitKey(1) & 0xFF
    if key == ord('y'): # exit on pressing 'y' 
        cv2.destroyAllWindows()
        break
    if key == ord('c'): # save picture on pressing 'c' 
        cv2.imwrite(str(imgCount) + ".jpg",frame)
        imgCount += 1

cap.release()