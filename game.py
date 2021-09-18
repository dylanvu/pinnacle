import pygame
import cv2
import numpy as np
from gameFuncts import *

# Set the pygame window size
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1850

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

BACKGROUND_COLOR = pygame.Color(251, 251, 248)
BLACK = pygame.Color(0, 0, 0)

# Intialize all relevant variables for the game
running = True
mouse = pygame.mouse.get_pos()
prevMouse = pygame.mouse.get_pos()

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

