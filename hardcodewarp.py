import cv2
import numpy as np

def HardCorrectWarping(SCREEN_DIMS):

    # correctWidth, correctHeight = 540,360
    correctWidth = SCREEN_DIMS[0]
    correctHeight = SCREEN_DIMS[1]

    points1 = np.float32([[150, 24], [517, 32], [153, 237], [513, 244]])
    points2 = np.float32([[0,0], [correctWidth, 0], [0, correctHeight], [correctWidth,correctHeight]])

    correctedMatrix = cv2.getPerspectiveTransform(points1, points2)
    return correctedMatrix