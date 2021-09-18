from turtle import color
import pygame
import cv2
import time
import numpy as np
from gameFuncts import *
from centroidScript import *
from CalibrateDot import *
from warpperspective import *

# OpenCV setup
cap = cv2.VideoCapture(0)
cameraMatrix = np.genfromtxt("./calibration/camera_matrix.txt")
dist = np.genfromtxt("./calibration/distortion.txt")
ret,frame = cap.read() # return a single frame in variable `frame`
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
h,w = frame.shape[:2]
newCameraMatrix, roi = cv2. getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h),1, (w,h))
perspectiveMatrix = None


# Set the pygame window size
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1850

# Define opencv frame size

FRAMESIZE = (1280,720)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

BACKGROUND_COLOR = pygame.Color(251, 251, 248)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
LIGHTGRAY = pygame.Color(139, 146, 153)
DARKGRAY = pygame.Color(42, 43, 43)

# Intialize all relevant variables for the game
running = True
# mouse = pygame.mouse.get_pos()
# prevMouse = pygame.mouse.get_pos()
prevPt = (None, None)
currPt = (None, None)
calibrated = False

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

while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cv2.destroyAllWindows()
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Panning
            if event.key == pygame.K_LEFT:
                Pan(screen, -10, 0, BACKGROUND_COLOR)
            if event.key == pygame.K_RIGHT:
                Pan(screen, 10, 0, BACKGROUND_COLOR)
            if event.key == pygame.K_UP:
                Pan(screen, 0, -10, BACKGROUND_COLOR)
            if event.key == pygame.K_DOWN:
                Pan(screen, 0, 10, BACKGROUND_COLOR)

    if (not calibrated):
        calibrationRadius = 20
        calibrationIncompleteColor = RED
        calibrationCompleteColor = BACKGROUND_COLOR
        # Step 1: draw top left dot and get centroid:
        # Clean up this ugly mess of if/else later?
        if (not topLeftcalibrate):
            DrawDot(screen, calibrationIncompleteColor, 0 + calibrationRadius, 0 + calibrationRadius, calibrationRadius)
            pygame.display.flip()
            topLeftdot = CalibrateDot(cap, frame, cameraMatrix, dist, newCameraMatrix, roi)
            topLeftcalibrate = True
        else:
            DrawDot(screen, calibrationCompleteColor, 0 + calibrationRadius, 0 + calibrationRadius, calibrationRadius)
            pygame.display.flip()
            if (not topRightcalibrate):
                DrawDot(screen, calibrationIncompleteColor, SCREEN_WIDTH - calibrationRadius, 0 + calibrationRadius, calibrationRadius)
                pygame.display.flip()
                topRightdot = CalibrateDot(cap, frame, cameraMatrix, dist, newCameraMatrix, roi)
                topRightcalibrate = True
            else:
                DrawDot(screen, calibrationCompleteColor, SCREEN_WIDTH - calibrationRadius, 0 + calibrationRadius, calibrationRadius)
                pygame.display.flip()
                if (not bottomLeftcalibrate):
                    DrawDot(screen, calibrationIncompleteColor, 0 + calibrationRadius, SCREEN_HEIGHT - calibrationRadius, calibrationRadius)
                    pygame.display.flip()
                    bottomLeftdot = CalibrateDot(cap, frame, cameraMatrix, dist, newCameraMatrix, roi)
                    bottomLeftcalibrate = True
                else:
                    DrawDot(screen, calibrationCompleteColor, 0 + calibrationRadius, SCREEN_HEIGHT - calibrationRadius, calibrationRadius)
                    pygame.display.flip()
                    if (not bottomRightcalibrate):
                        DrawDot(screen, calibrationIncompleteColor, SCREEN_WIDTH - calibrationRadius, SCREEN_HEIGHT - calibrationRadius, calibrationRadius)
                        pygame.display.flip()
                        bottomRightdot = CalibrateDot(cap, frame, cameraMatrix, dist, newCameraMatrix, roi)
                        bottomRightcalibrate = True
                    else:
                        DrawDot(screen, calibrationCompleteColor, SCREEN_WIDTH - calibrationRadius, SCREEN_HEIGHT - calibrationRadius, calibrationRadius)
                        pygame.display.flip()
                        calibrated = True
                        perspectiveMatrix = CorrectWarping(topLeftdot, topRightdot, bottomLeftdot, bottomRightdot)
    else:
        # After we are done calibrating, we have our main drawing and detection stuff
        ust = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
        x, y, w, h = roi
        ust = ust[y:y+h, x:x+w]

        # correct warping
        outputFrame = cv2.warpPerspective(frame, perspectiveMatrix, FRAMESIZE)
        cv2.imshow(outputFrame)
        ((cX,cY),color) = centroidScript(outputFrame)
        print(((cX,cY),color))
        currPt = (cX, cY)
        if (prevPt == (None, None)):
                prevPt = currPt
        else:
            if (color == "red"):
                InterpolatePoints(screen, BLACK, prevPt[0], prevPt[1], currPt[0], currPt[1], 5)
                pygame.display.flip()
            elif (color == "green"):
                InterpolatePoints(screen, BACKGROUND_COLOR, prevPt[0], prevPt[1], currPt[0], currPt[1], 5)
                pygame.display.flip()

    if (fillAftercalibrate):
        screen.fill(BACKGROUND_COLOR)
        fillAftercalibrate = False

    # Check for mouse down and draw if pressed
    # if pygame.mouse.get_pressed()[0]:
    #     InterpolatePoints(screen, BLACK, prevMouse[0], prevMouse[1], mouse[0], mouse[1], 5)

    # Once we receive coordinates:
    # if (existsCoordinates) and (draw):
    #     DrawDot(screen, BLACK, x coord, y coord, 10)

    # if (existsCoordinates) and (erase):
    #     DrawDot(screen, ERASE COLOR, x coord, y coord, 10)

    # Save previous mouse and get new mouse for interpolation of points
    # prevMouse = mouse
    # mouse = pygame.mouse.get_pos()
    

    # cv2.imshow('Capturing Video',ust) #display the captured image

    # Flip the display
    pygame.display.flip()
# Step 1: Boot up Pygame screen
# Step 2: Apply camera matrix
# Step 2: Display points
# Step 3: get perspective matrix
# Step 4: Get frames and apply perspective matrix