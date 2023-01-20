import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
cap = cv.VideoCapture(0)

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
countdown=0
while(1):
    # Take each frame
    _, frame = cap.read()
    #dominantColor
    crop=frame[105:255,195:445]
    if countdown == 0:
        img = cv.cvtColor(crop, cv.COLOR_BGR2RGB)
        img = img.reshape((img.shape[0] * img.shape[1],3))
        clt = KMeans(n_clusters=1) #cluster number
        clt.fit(img)
        hist = find_histogram(clt)
        bar = plot_colors2(hist, clt.cluster_centers_)
        bar = cv.cvtColor(bar, cv.COLOR_RGB2BGR)
        cv.imshow("bar",bar)
    
        countdown = 100
    cv.imshow("crop",crop)
    countdown=countdown-1
    #cv.imshow('frame',frame)
    #cv.imshow('mask',mask)
    #cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()