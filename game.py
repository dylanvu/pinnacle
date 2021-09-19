from turtle import color
import pygame
import cv2
import time
import math
import numpy as np
from gameFuncts import *
from centroidScript import *
from CalibrateDot import *
from warpperspective import *
from hardcodewarp import *

# Variables to change on setup
calibrated = True
SCREEN_HEIGHT = 480
SCREEN_WIDTH = 720
SCREEN_DIMS = (SCREEN_WIDTH, SCREEN_HEIGHT)
# remember to edit hard warped .py

# OpenCV setup
cap = cv2.VideoCapture(0)
cameraMatrix = np.genfromtxt("./calibration/camera_matrix.txt")
dist = np.genfromtxt("./calibration/distortion.txt")
ret,frame = cap.read() # return a single frame in variable `frame`
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# cv2.imshow("shit", frame)
h,w = frame.shape[:2]
newCameraMatrix, roi = cv2. getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h),1, (w,h))
perspectiveMatrix = HardCorrectWarping(SCREEN_DIMS)


# # Set the pygame window size
# SCREEN_HEIGHT = 1000
# SCREEN_WIDTH = 1850

# SCREEN_HEIGHT = 360
# SCREEN_WIDTH = 540



# Define opencv frame size

FRAMESIZE = (1080,720)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# BACKGROUND_COLOR = pygame.Color(251, 251, 248)
BACKGROUND_COLOR = pygame.Color(0, 0, 0)
# BLACK = pygame.Color(0, 0, 0)
# BLACK = pygame.Color(255,255,255)
WHITE = pygame.Color(251, 251, 248)
RED = pygame.Color(255, 0, 0)
BLACK = WHITE
GREEN = pygame.Color(0, 255, 0)
LIGHTGRAY = pygame.Color(139, 146, 153)
DARKGRAY = pygame.Color(42, 43, 43)

# Intialize all relevant variables for the game
running = True
# mouse = pygame.mouse.get_pos()
# prevMouse = pygame.mouse.get_pos()
prevPt = (None, None)
currPt = (None, None)
noneCounter = 0

# for calibration purposes
topLeftdot = (None,None)
topLeftcalibrate = False
topRightdot = (None,None)
topRightcalibrate = False
bottomLeftdot = (None,None)
bottomLeftcalibrate = False
bottomRightdot = (None,None)
bottomRightcalibrate = False

fillAftercalibrate = False

screen.fill(BACKGROUND_COLOR)
# cv2.imshow("pain", frame)
while running:


    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         cv2.destroyAllWindows()
    #         running = False
        
    #     if event.type == pygame.KEYDOWN:
    #         # Panning
    #         # if event.key == pygame.K_LEFT:
    #         #     Pan(screen, -10, 0, BACKGROUND_COLOR)
    #         # if event.key == pygame.K_RIGHT:
    #         #     Pan(screen, 10, 0, BACKGROUND_COLOR)
    #         # if event.key == pygame.K_UP:
    #         #     Pan(screen, 0, -10, BACKGROUND_COLOR)
    #         # if event.key == pygame.K_DOWN:
    #         #     Pan(screen, 0, 10, BACKGROUND_COLOR)
    #         if event.key == pygame.K_UP:
    #             screen.fill(BACKGROUND_COLOR)
    #         if event.key == pygame.K_q:
    #             cv2.destroyAllWindows()
    #             running = False
#     ret2,frame2 = cap.read()
#     cv2.imshow("depression", frame)
    if (not calibrated):
        # After we are done calibrating, we have our main drawing and detection stuff
        ret,frame = cap.read()
        ust = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
        x, y, w, h = roi
        ust = ust[y:y+h, x:x+w]

        # correct warping
#         print(ust)
        # outputFrame = cv2.warpPerspective(ust, perspectiveMatrix, FRAMESIZE)
#         cv2.imshow("output",outputFrame)
        ((cX,cY),color) = centroidScript(ust) # for no warping
        # ((cX,cY),color) = centroidScript(outputFrame) # for warping
#         cv2.imshow("frame",ust)
        #EMERGENCY PRINT
        print(((cX,cY),color))
        currPt = (cX, cY)
        if (currPt == (None, None)):
            noneCounter += 1
            if (noneCounter >= 5):
                prevPt = (None, None)
        else:
            noneCounter = 0
        if (prevPt == (None, None)):
                prevPt = currPt
        else:
            if (color == "red"):
                # If red is detected, draw
                InterpolatePoints(screen, BLACK, prevPt[0], prevPt[1], currPt[0], currPt[1], 5)
                pygame.display.flip()
                prevPt = currPt
            elif (color == "green"):
                # If green is detected, erase
                screen.fill(BACKGROUND_COLOR)
                # InterpolatePoints(screen, BACKGROUND_COLOR, prevPt[0], prevPt[1], currPt[0], currPt[1], 20)
                # pygame.display.flip()
                # prevPt = currPt
    else:
        # After we are done calibrating, we have our main drawing and detection stuff
        ret,frame = cap.read()
        ust = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
        x, y, w, h = roi
        ust = ust[y:y+h, x:x+w]

        # correct warping
#         print(ust)
        outputFrame = cv2.warpPerspective(ust, perspectiveMatrix, FRAMESIZE)
#         cv2.imshow("output",outputFrame)
        # ((cX,cY),color) = centroidScript(ust) # for no warping
        ((cX,cY),color) = centroidScript(outputFrame) # for warping
#         cv2.imshow("frame",ust)
        #EMERGENCY PRINT
        # print(((cX,cY),color))
        currPt = (cX, cY)
        if (currPt == (None, None)):
            noneCounter += 1
            if (noneCounter >= 5):
                prevPt = (None, None)
        else:
            noneCounter = 0
        if (prevPt == (None, None)):
                prevPt = currPt
        else:
            if (color == "red"):
                # If red is detected, draw
                InterpolatePoints(screen, BLACK, prevPt[0], prevPt[1], currPt[0], currPt[1], 5)
                pygame.display.flip()
                prevPt = currPt
            elif (color == "green"):
                # If green is detected, erase
                screen.fill(BACKGROUND_COLOR)
                # InterpolatePoints(screen, BACKGROUND_COLOR, prevPt[0], prevPt[1], currPt[0], currPt[1], 20)
                # pygame.display.flip()
                # prevPt = currPt

    if (fillAftercalibrate):
        screen.fill(BACKGROUND_COLOR)
        fillAftercalibrate = False

    if pygame.mouse.get_pressed()[0]:
        cv2.destroyAllWindows()
        running = False

    # Flip the display
    pygame.display.flip()