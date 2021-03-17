# -*- coding: utf-8 -*-

import cv2
import numpy as np
from copy import deepcopy

#creates named Window
cv2.namedWindow("Image")

#loads image
img = cv2.imread("Schwarz.png")

#scale
scale = 44

width = int(img.shape[1] * scale/100)
height = int(img.shape[0] * scale/100)

#dsize
dsize = (width, height)

#scales the image
img = cv2.resize(img, dsize)

cv2.imshow("Image", img)

#Eventhandler Class for param to avoid global variables, 
#a dictionary is (probably) better here but hey, I can define a class :D
class EHC:
    def __init__(self):
        self.entry={"poi1" : [], "poi2" : [], "mindistIdx" : None, "img" : img,
                    "set" : False}

def onMouse(event, x, y, flags, param:EHC):

    #The points are set by double clicking left mouse button
    if len(param.entry["poi1"]) < 4 and event == cv2.EVENT_LBUTTONDBLCLK:
        #sets initial 4 points and appends them to a list
        cv2.circle(img, (x, y), 5, (0, 255, 0), 2)
        cv2.imshow("Image", param.entry["img"])
        print(x, y)
        param.entry["poi1"].append([x,y])
    
    #Initializes Lists for the homomorphy calculation
    if  param.entry["set"] == False and len(param.entry["poi1"]) == 4:
        param.entry["set"] = True
        param.entry["poi1"] = np.float32(param.entry["poi1"])
        param.entry["poi2"] = deepcopy(param.entry["poi1"]) 
        
    #The point to drag is set by again double clicking the left mouse button,
    #in which case the closest one of the four previous points is chosen
    elif len(param.entry["poi1"]) == 4 and event == cv2.EVENT_LBUTTONDBLCLK:   
        #print("Oh behave!")

        mindist = float("inf")
        param.entry["mindistIdx"] = None
        
        cv2.circle(img, (x, y), 5, (0, 0, 255), 2)
        curMouseCoords = [x, y]
        for i in range(len(param.entry["poi1"])):
            curPoiDist = np.linalg.norm(param.entry["poi1"][i] - curMouseCoords)
            if curPoiDist < mindist:
                mindist = curPoiDist
                param.entry["mindistIdx"] = i
        
        print("Closest Position in list: ", param.entry["mindistIdx"])
        print("Mouse: ",curMouseCoords,"\n", "Closest Listpoint: ", 
              param.entry["poi1"][param.entry["mindistIdx"]])

        HomMat, st = cv2.findHomography(param.entry["poi1"], param.entry["poi2"])
        resImg = cv2.warpPerspective(param.entry["img"], HomMat, dsize)
        cv2.imshow("Image", resImg)
       
        
    #part of the code where the warping of the image occurs by pressing down
    #the right mouse button and gently dragging the mousey
    elif (len(param.entry["poi1"]) == 4 and flags == cv2.EVENT_FLAG_RBUTTON and 
            event == cv2.EVENT_MOUSEMOVE):
        #print("squiggling right now :D")
        
        param.entry["poi2"][param.entry["mindistIdx"]] = [x, y]
        HomMat, st = cv2.findHomography(param.entry["poi1"], param.entry["poi2"])
        resImg = cv2.warpPerspective(param.entry["img"], HomMat, dsize)
        cv2.imshow("Image", resImg)
     
#Sets param to the Class with the parameters
param = EHC()
#Starts the MouseCallback in the window "Image", 
#with the eventhandler onMouse, using param as the Class EHC
cv2.setMouseCallback("Image", onMouse, param)    

#Exit with Esc key
cv2.waitKey(0)
cv2.destroyAllWindows()
