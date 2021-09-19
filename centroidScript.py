import numpy as np
import cv2
import time
#will output x,y,colorString
def centroidScript(frame):
    lower_color_green = (0, 90, 20)
    upper_color_green = (90,255,135)
    maskGreen = cv2.inRange(frame,lower_color_green,upper_color_green)
    # res1 = cv2.bitwise_and(frame,frame, mask= maskGreen)

    mask_rgb = cv2.cvtColor(maskGreen,cv2.COLOR_GRAY2BGR)
    imgGray = cv2.cvtColor(mask_rgb, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(imgGray, 200, 255, cv2.THRESH_BINARY)
    countG = cv2.countNonZero(thresh)
    #
    # countG =0

    lower_color_red = (40, 10, 120) #40, 0 120
    upper_color_red = (104, 83,255)
    maskRed = cv2.inRange(frame,lower_color_red,upper_color_red)
    # res2 = cv2.bitwise_and(frame,frame, mask= maskRed)
    mask_rgb = cv2.cvtColor(maskRed,cv2.COLOR_GRAY2BGR)
    imgGray1 = cv2.cvtColor(mask_rgb, cv2.COLOR_BGR2GRAY)
    _, thresh1 = cv2.threshold(imgGray1, 200, 255, cv2.THRESH_BINARY)

    countR = cv2.countNonZero(thresh1)
    # print(countR)

    res = cv2.bitwise_or(thresh,thresh1)
    cX = -1
    cY = -1
#     cv2.imshow("res",res)
    try:
        cnts, _ = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if len(cnts) > 0:
            # cnt = sorted(cnts, key=cv2.contourArea)
            c1 = cnts[0]
            (cX,cY),radius = cv2.minEnclosingCircle(c1)
            cX = int(cX)
            cY = int(cY)
            radius = int(radius)
            # cv2.drawContours(frame, c1, -1, (255, 0, 0), 5) TODO
        
    except:
        cX = -1
        cY = -1
    # print(countG,countR)
    if countG > 30:
        return((cX,cY),"green")
    elif countR > 25:
        return((cX,cY),"red")
    else:
        return((None,None),None)
