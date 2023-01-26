import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
cap = cv.VideoCapture(0)

def maxAreaCnt(cnt):
    areaMax=0
    areaInd=0
    for i in range(0,len(cnt)):
        area = cv.contourArea(cnt[i])
        if area >= areaMax:
            areaMax=area
            areaInd=i
            continue
        else:
            continue
    return areaInd      
while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_HSV = np.array([13,100,100])
    upper_HSV = np.array([103,255,255])

    lower_BGR= np.array([146,120,19])
    upper_BGR= np.array([255,199,110])
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_HSV, upper_HSV)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    
    #BoundingBoxStuff
    contours,hierarchy = cv.findContours(mask, 1, 2)
    if len(contours)==0:
        continue
    else:
        cnt = contours[maxAreaCnt(contours)]

    #cv.drawContours(res,[cnt],-1,(0,0,255),2)
    
    x,y,w,h = cv.boundingRect(cnt)
    cv.rectangle(res,(x,y),(x+w,y+h),(0,255,0),2)

    
    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()