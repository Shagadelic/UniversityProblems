#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor
Author: Shagadelic
Date: Jan 27.1.2021
Groove: 3/10
Weather: still kinda cold
"""
import cv2
import numpy as np
from copy import deepcopy

#creates named Window
cv2.namedWindow("Image")

#loads image
img = cv2.imread("koreanSigns.png")
#grayscale image
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("Image", img)

#dummy function for the trackbar, since only the value is needed
def thresh_change(trsh):
    pass

#creates trackbar to set the threshold with
cv2.createTrackbar("Threshold", "Image", 95, 100, thresh_change)
#sets threshold min to 90, because setting it lower will color everything
cv2.setTrackbarMin("Threshold", "Image", 90)

#Mouse callback, used to set the two points for the rectangle 
def onMouse(event, x, y, flags, param:{}):

    #The points are set by double clicking left mouse button
    #They are supposed to be the upper/lower left/right corners of the template
    if len(param["poi"]) < 2 and event == cv2.EVENT_LBUTTONDBLCLK:
        #sets initial 4 points and appends them to a list
        cv2.circle(img, (x, y), 5, (0, 255, 0), 2)
        cv2.imshow("Image", param["img"])
        print(x, y)
        param["poi"].append([x,y])
    
    #part of the code where the warping of the image occurs by pressing down
    #the right mouse button and gently dragging the mousey
    elif (len(param["poi"]) == 2):
        #gets template for the matching
        param["template"] = param["img_g"][
                                              min(param["poi"][0][1], param["poi"][1][1]):
                                              max(param["poi"][0][1], param["poi"][1][1]), 
                                              min(param["poi"][0][0], param["poi"][1][0]):
                                              max(param["poi"][0][0], param["poi"][1][0])
                                          ]      
        #gets dimensions of the template
        template_width, template_width = param["template"].shape[::-1]
        #uses normalized cross-correlation to find the points
        res = cv2.matchTemplate(param["img_g"], param["template"], cv2.TM_CCORR_NORMED) 
        
        #Loop for the trackbar
        while(1):
            
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                cv2.destroyAllWindows()
        
            #gets current threshold from the trackbar
            param["threshold"] = int(cv2.getTrackbarPos("Threshold",'Image'))/100
            #gets the points that fulfill the threshold requirement
            location = np.where(res > param["threshold"])
            #makes a copy of the window, to repaint it if the threshold changes
            image = deepcopy(param["img"])
            #puts green rectangles around the points above
            for point in zip(*location[::-1]):
                cv2.rectangle(
                    image, 
                    point, 
                    (point[0] + template_width, point[1] + template_width), 
                    (0, 255, 0), 
                    2
                    )
            cv2.imshow("Image", image)
        
#dictionary with a field for points, one for the selected image part
#and one for the image, image in grayscale and the threshold for the correlation
#to be used as param.
param = {"poi" : [], "img" : img, "img_g" : img_gray, "threshold" : 0.96}

cv2.setMouseCallback("Image", onMouse, param) 

cv2.waitKey(0)
cv2.destroyAllWindows()