import cv2
import numpy as np

def HardCorrectWarping(SCREEN_DIMS):

    # correctWidth, correctHeight = 540,360
    correctWidth = SCREEN_DIMS[0]
    correctHeight = SCREEN_DIMS[1]

    points1 = np.float32([[146, 78], [518, 95], [142, 295], [516, 311]])
    points2 = np.float32([[0,0], [correctWidth, 0], [0, correctHeight], [correctWidth,correctHeight]])

    correctedMatrix = cv2.getPerspectiveTransform(points1, points2)
    return correctedMatrix