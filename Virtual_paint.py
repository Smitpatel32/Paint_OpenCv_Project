# importing important modules
from turtle import color
import cv2 as cv
import numpy as np

# frame size of the webcam screen.
frameW = 640
frameH = 480


cap = cv.VideoCapture(0)

# id 3 for width and 4 for height
cap.set(3,frameW)
cap.set(4,frameH)

# brightness id =10
cap.set(10,150)  

# HSV Min - HSV Max Values for different colors
myColor = [[84,81,52,133,139,231],
           [0,74,129,30,178,231]]

# BGR Values corresponding to the HSV values
colors = [[255,0,0],[51,255,255]]

#Empty list for points to draw
myPoints = []

# function to draw on the screen
def drawOnCanv(myPoints,colors):
    for point in myPoints:
        cv.circle(framec,(point[0],point[1]),10,colors[point[2]],cv.FILLED)

# function to find contours 
def gcon(img):
    contour,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for c in contour:
        area = cv.contourArea(c)
        if area>500:
            # cv.drawContours(framec,c,-1,(255,0,255),1)
            edg = cv.arcLength(c,True)
            approx = cv.approxPolyDP(c,0.04*edg,True)
            x,y,w,h= cv.boundingRect(approx)
    return x+w//2,y

# Function to find color and Object detection
def findColor(img,myColor,col):
    imghsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    count = 0
    points = []

    for color in myColor:

# first 3 values of myColor as lower and last 3 as higher values 
        lower = np.array([color[0:3]])
        higher = np.array([color[3:6]])
        mask = cv.inRange(imghsv,lower,higher)
        x,y=gcon(mask)
        cv.circle(framec,(x,y),10,col[count],cv.FILLED)
        if x!=0 and y!=0:
            points.append([x,y,count])
        count+=1

# returning x,y and count values
    return points   
 
           
# Loop to display frames.
while True:
    success,frame = cap.read()
    framec = frame.copy()
    newpoint = findColor(frame,myColor,colors)
    if len(newpoint)!=0:
        for newP in newpoint:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanv(myPoints,colors)
    cv.imshow('Web',framec)

    if cv.waitKey(1) & 0xFF == ord('d'):
        break;
