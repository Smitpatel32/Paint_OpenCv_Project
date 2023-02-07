from turtle import color
import cv2 as cv
import numpy as np

frameW = 640
frameH = 480

# brightness id =10
# id 3 for width and 4 for height
cap = cv.VideoCapture(0)
cap.set(3,frameW)
cap.set(4,frameH)
cap.set(10,150)  

myColor = [[84,81,52,133,139,231],
           [0,74,129,30,178,231]]
colors = [[255,0,0],[51,255,255]]

myPoints = []

def drawOnCanv(myPoints,colors):
    for point in myPoints:
        cv.circle(framec,(point[0],point[1]),10,colors[point[2]],cv.FILLED)


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

def findColor(img,myColor,col):
    imghsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    count = 0
    points = [] 
    for color in myColor:
        lower = np.array([color[0:3]])
        higher = np.array([color[3:6]])
        mask = cv.inRange(imghsv,lower,higher)
        # cv.imshow(str(color[0]),mask) 
        x,y=gcon(mask)
        cv.circle(framec,(x,y),10,col[count],cv.FILLED)
        if x!=0 and y!=0:
            points.append([x,y,count])
        count+=1
    return points   
 
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