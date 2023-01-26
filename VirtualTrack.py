import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
def nothing(x):
    pass
cv.namedWindow("Trackbars")
cv.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv.createTrackbar("U - H", "Trackbars", 0, 179, nothing)

while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    l_h = cv.getTrackbarPos("L - H", "Trackbars")
    u_h = cv.getTrackbarPos("U - H", "Trackbars")
    lower = np.array([l_h,100,100])
    upper= np.array([u_h,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()