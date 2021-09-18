import cv2

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
imgCount = 0 # Number of images

while(True):
    ret,frame = cap.read() # return a single frame in variable `frame`
    cv2.imshow('Capturing Video',frame) #display the captured image
    key = cv2.waitKey(1) & 0xFF
    if key == ord('y'): # exit on pressing 'y' 
        cv2.destroyAllWindows()
        break
    if key == ord('c'): # save picture on pressing 'c' 
        cv2.imwrite(str(imgCount) + ".jpg",frame)
        imgCount += 1

cap.release()