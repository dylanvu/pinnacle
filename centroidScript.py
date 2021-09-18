import numpy as np
import cv2
import time
#will output x,y,colorString
def centroidScript():
    lower_color_green = (10, 100, 35) #BGR
    upper_color_green = (35,255,90)
    maskGreen = cv2.inRange(frame,lower_color_green,upper_color_green)
    res1 = cv2.bitwise_and(frame,frame, mask= maskGreen)

    mask_rgb = cv2.cvtColor(maskGreen,cv2.COLOR_GRAY2BGR)
    imgGray = cv2.cvtColor(mask_rgb, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(imgGray, 200, 255, cv2.THRESH_BINARY)
    countG = cv2.countNonZero(thresh)


    lower_color_red = (40, 0, 180)
    upper_color_red = (104, 83,220)
    maskRed = cv2.inRange(frame,lower_color_red,upper_color_red)
    res2 = cv2.bitwise_and(frame,frame, mask= maskRed)
    mask_rgb = cv2.cvtColor(maskRed,cv2.COLOR_GRAY2BGR)
    imgGray1 = cv2.cvtColor(mask_rgb, cv2.COLOR_BGR2GRAY)
    _, thresh1 = cv2.threshold(imgGray1, 200, 255, cv2.THRESH_BINARY)

    countR = cv2.countNonZero(thresh1)

    res = cv2.bitwise_or(thresh,thresh1)
    cX = -1
    cY = -1
    # cv2.imshow("res",thresh)
    try:
        cnts, hierarchy = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if len(cnts)> 1:
            cnt = sorted(cnts, key=cv2.contourArea)
            c1 = cnts[0]
            (cX,cY),radius = cv2.minEnclosingCircle(c1)
            cX = int(cX)
            cY = int(cY)
            radius = int(radius)
            cv2.drawContours(frame, c1, -1, (255, 0, 0), 1)
    except:
        cX = -1
        cY = -1
    print(countG,countR)
    if countG > 1:
        return((cX,cY),"green")
    elif countR > 1:
        return((cX,cY),"red")
    else:
        return((None,None),None)
