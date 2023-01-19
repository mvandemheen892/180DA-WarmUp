import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
def nothing(x):
    pass
cv.namedWindow("Trackbars")
cv.createTrackbar("L - R", "Trackbars", 0, 255, nothing)
cv.createTrackbar("U - R", "Trackbars", 0, 255, nothing)
cv.createTrackbar("L - G", "Trackbars", 0, 255, nothing)
cv.createTrackbar("U - G", "Trackbars", 0, 255, nothing)
cv.createTrackbar("L - B", "Trackbars", 0, 255, nothing)
cv.createTrackbar("U - B", "Trackbars", 0, 255, nothing)

while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    #hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    l_r = cv.getTrackbarPos("L - R", "Trackbars")
    u_r = cv.getTrackbarPos("U - R", "Trackbars")
    l_g = cv.getTrackbarPos("L - G", "Trackbars")
    u_g = cv.getTrackbarPos("U - G", "Trackbars")
    l_b = cv.getTrackbarPos("L - B", "Trackbars")
    u_b = cv.getTrackbarPos("U - B", "Trackbars")
    lower = np.array([l_b,l_g,l_r])
    upper= np.array([u_b,u_g,u_r])
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(frame, lower, upper)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()