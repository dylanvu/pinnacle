import pygame
import cv2
import time
import numpy as np
from gameFuncts import *

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
mouse = pygame.mouse.get_pos()
prevMouse = pygame.mouse.get_pos()
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
            
    # If we have coordinates to calibrate
    if pygame.key.get_pressed()[pygame.K_q]:
        calibrationCoords = mouse
    else:
        calibrationCoords = (None, None)

    if (not calibrated):
        # Draw the four dots
        calibrationRadius = 20
        calibrationIncompleteColor = LIGHTGRAY
        calibrationCompleteColor = DARKGRAY
        if (not topLeftcalibrate):
            DrawDot(screen, calibrationIncompleteColor, 0 + calibrationRadius, 0 + calibrationRadius, calibrationRadius)
        else:
            DrawDot(screen, calibrationCompleteColor, 0 + calibrationRadius, 0 + calibrationRadius, calibrationRadius)

        if (not topRightcalibrate):
            DrawDot(screen, calibrationIncompleteColor, SCREEN_WIDTH - calibrationRadius, 0 + calibrationRadius, calibrationRadius)
        else:
            DrawDot(screen, calibrationCompleteColor, SCREEN_WIDTH - calibrationRadius, 0 + calibrationRadius, calibrationRadius)

        if (not bottomLeftcalibrate):
            DrawDot(screen, calibrationIncompleteColor, 0 + calibrationRadius, SCREEN_HEIGHT - calibrationRadius, calibrationRadius)
        else:
            DrawDot(screen, calibrationCompleteColor, 0 + calibrationRadius, SCREEN_HEIGHT - calibrationRadius, calibrationRadius)

        if (not bottomRightcalibrate):
            DrawDot(screen, calibrationIncompleteColor, SCREEN_WIDTH - calibrationRadius, SCREEN_HEIGHT - calibrationRadius, calibrationRadius)
        else:
            DrawDot(screen, calibrationCompleteColor, SCREEN_WIDTH - calibrationRadius, SCREEN_HEIGHT - calibrationRadius, calibrationRadius)
        if (calibrationCoords):
            # Check if calibration has finished
            if (topLeftdot != (None, None) and topRightdot != (None, None) and bottomLeftdot != (None, None) and bottomRightdot != (None, None)):
                calibrated = True
                fillAftercalibrate = True
                print("Bingo!")
            else:
                # Case 1: top left
                if (calibrationCoords[0] != None and calibrationCoords[1] != None):
                    if (calibrationCoords[0] <= FRAMESIZE[0] / 2 and calibrationCoords[1] <= FRAMESIZE[1] / 2):
                        topLeftdot = (calibrationCoords[0], calibrationCoords[1])
                        topLeftcalibrate = True
                        print("topleft")

                    # Case 2: top right
                    if (calibrationCoords[0] > FRAMESIZE[0] / 2 and calibrationCoords[1] < FRAMESIZE[1] / 2):
                        topRightdot = (calibrationCoords[0], calibrationCoords[1])
                        topRightcalibrate = True
                        print("topright")
                    
                    # Case 3: bottom left
                    if (calibrationCoords[0] <= FRAMESIZE[0] / 2 and calibrationCoords[1] > FRAMESIZE[1] / 2):
                        bottomLeftdot = (calibrationCoords[0], calibrationCoords[1])
                        bottomLeftcalibrate = True
                        print("botleft")

                    # Case 4: bottom right
                    if (calibrationCoords[0] > FRAMESIZE[0] / 2 and calibrationCoords[1] > FRAMESIZE[1] / 2):
                        bottomRightdot = (calibrationCoords[0], calibrationCoords[1])
                        bottomRightcalibrate = True
                        print("botright")

    if (fillAftercalibrate):
        screen.fill(BACKGROUND_COLOR)
        fillAftercalibrate = False

    # Check for mouse down and draw if pressed
    if pygame.mouse.get_pressed()[0]:
        InterpolatePoints(screen, BLACK, prevMouse[0], prevMouse[1], mouse[0], mouse[1], 5)

    # Once we receive coordinates:
    # if (existsCoordinates) and (draw):
    #     DrawDot(screen, BLACK, x coord, y coord, 10)

    # if (existsCoordinates) and (erase):
    #     DrawDot(screen, ERASE COLOR, x coord, y coord, 10)

    # Save previous mouse and get new mouse for interpolation of points
    prevMouse = mouse
    mouse = pygame.mouse.get_pos()

    # Flip the display
    pygame.display.flip()


# Step 1: Boot up Pygame screen
# Step 2: Display points
# Step 3: get perspective matrix
# Step 4: Get frames and apply perspective matrix