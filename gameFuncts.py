import pygame
import math

def DrawDot(screen, color, x, y, radius):
    # Basic function for drawing a circle with parameters
    pygame.draw.circle(screen, color, (x, y), radius)

def InterpolatePoints(screen, color, x1, y1, x2, y2, thickness):
    pygame.draw.aaline(screen, color, (x1, y1), (x2, y2))

    # Deal with the larger width
    for num in range(thickness):
        pygame.draw.aaline(screen, color, (x1 + num, y1), (x2 + num, y2))
        pygame.draw.aaline(screen, color, (x1 - num, y1), (x2 - num, y2))
        pygame.draw.aaline(screen, color, (x1, y1 + num), (x2, y2 + num))
        pygame.draw.aaline(screen, color, (x1, y1 - num), (x2, y2 - num))

    # Maybe: create circles instead? Make smoother on edges of interpolation
    # Check if we're moving to the left/right and up/down and don't draw depending on the direction

def Pan(screen, xshift, yshift, fillColor):
    temp_surf = pygame.Surface.copy(screen)
    screen.fill(fillColor)
    screen.blit(temp_surf, (xshift, yshift))