import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans
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

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_HSV = np.array([81,100,100])
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

    #dominantColor
    #crop=frame[105:255,195:445]
    #cv.imshow("crop",crop)
    #img = cv.cvtColor(crop, cv.COLOR_BGR2RGB)
    #img = img.reshape((img.shape[0] * img.shape[1],3))
    #clt = KMeans(n_clusters=5) #cluster number
    #clt.fit(img)
    #hist = find_histogram(clt)
    #bar = plot_colors2(hist, clt.cluster_centers_)
    #cv.imshow("bar",bar)









    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()