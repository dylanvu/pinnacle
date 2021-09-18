import cv2
import numpy as np

def CorrectWarping(topLeft, topRight, bottomLeft, bottomRight):

    topLeftx = topLeft[0]
    topLefty = topLeft[1]

    topRightx = topRight[0]
    topRighty = topRight[1]

    bottomLeftx = bottomLeft[0]
    bottomLefty = bottomLeft[1]

    bottomRightx = bottomRight[0]
    bottomRighty = bottomRight[1]

    correctWidth, correctHeight = 1280,720

    points1 = np.float32([[topLeftx, topLefty], [topRightx, topRighty], [bottomLeftx, bottomLefty], [bottomRightx, bottomRighty]])
    points2 = np.float32([[0,0], [correctWidth, 0], [0, correctHeight], [correctWidth,correctHeight]])

    correctedMatrix = cv2.getPerspectiveTransform(points1, points2)
    return correctedMatrix