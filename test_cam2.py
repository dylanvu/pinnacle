import numpy as np
import cv2
import time


cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop)
cameraMatrix = np.genfromtxt("/home/pi/Documents/pinnacle/calibration/camera_matrix.txt") #TODO
dist = np.genfromtxt("/home/pi/Documents/pinnacle/calibration/distortion.txt") #TODO

ret,frame = cap.read()
h,w = frame.shape[:2]
color = "none"
newCameraMatrix, roi = cv2. getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h),1, (w,h)) #TODO

while(True):
    ret,frame = cap.read() # return a single frame in variable `frame`
    frame = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)  #TODO

    cv2.imshow('Capturing Video',frame) #display the captured image

    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # maskGreen = cv2.inRange(hsv, lower_range, upper_range)
    lower_color_green = (0, 90, 20)
    upper_color_green = (90,255,135)
    maskGreen = cv2.inRange(frame,lower_color_green,upper_color_green)
    res1 = cv2.bitwise_and(frame,frame, mask= maskGreen)

    mask_rgb = cv2.cvtColor(maskGreen,cv2.COLOR_GRAY2BGR)
    imgGray = cv2.cvtColor(mask_rgb, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(imgGray, 200, 255, cv2.THRESH_BINARY)
    countG = cv2.countNonZero(thresh)
    #
    # countG =0
# 
#     lower_color_red = (40, 15, 110) #180
#     upper_color_red = (90, 70,255)
#     maskRed = cv2.inRange(frame,lower_color_red,upper_color_red)
#     res2 = cv2.bitwise_and(frame,frame, mask= maskRed)
#     mask_rgb = cv2.cvtColor(maskRed,cv2.COLOR_GRAY2BGR)
#     imgGray1 = cv2.cvtColor(mask_rgb, cv2.COLOR_BGR2GRAY)
#     _, thresh1 = cv2.threshold(imgGray1, 200, 255, cv2.THRESH_BINARY)
# 
#     countR = cv2.countNonZero(thresh1)


    lower_color_red = (40, 10, 120) #40, 0 120
    upper_color_red = (104, 83,255)
    maskRed = cv2.inRange(frame,lower_color_red,upper_color_red)
    res2 = cv2.bitwise_and(frame,frame, mask= maskRed)
    mask_rgb = cv2.cvtColor(maskRed,cv2.COLOR_GRAY2BGR)
    imgGray1 = cv2.cvtColor(mask_rgb, cv2.COLOR_BGR2GRAY)
    _, thresh1 = cv2.threshold(imgGray1, 200, 255, cv2.THRESH_BINARY)

    countR = cv2.countNonZero(thresh1)

    res = cv2.bitwise_or(thresh,thresh1)
    cX = -1
    cY = -1
    cv2.imshow("res",res)
    try:
        cnts, hierarchy = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if len(cnts)> 0:
            cnts = sorted(cnts, key=cv2.contourArea)
            c1 = cnts[0]
            (cX,cY),radius = cv2.minEnclosingCircle(c1)
            cX = int(cX)
            cY = int(cY)
            radius = int(radius)
            cv2.drawContours(frame, c1, -1, (255, 0, 0), 10)
    except:
        cX = -1
        cY = -1
    print(countG,countR)
    if countG > 20:
        print(cX,cY,"green")
    elif countR > 0:
        print(cX,cY,"red")
    else:
        print(cX,cY,"none")

    # print(cX,cY)

    cv2.imshow("fr",frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('y'): # exit on pressing 'y'
        cv2.destroyAllWindows()
        break
cap.release()

