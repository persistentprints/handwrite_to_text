#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 20:39:50 2022

@author: gustavo
"""

import cv2 
import numpy as np
 
image = cv2.imread('img.png', cv2.IMREAD_UNCHANGED)
image =  image[:,:,3]
data = np.zeros((600, 800, 3), dtype=np.uint8)
contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

print(len(contours))
#image = (255-image)
horizontal_array = np.empty(image.shape[1], int)

for line in range(image.shape[1]):
    result = 0
    for pixel in range(image.shape[0]):
        if(image[pixel,line] > 1):
            result = result + 1
    horizontal_array[line] = result    

count = 0   
characters = [] 
while count != image.shape[1]-1:
    character = []
    while (horizontal_array[count] == 0) & (count != image.shape[1]-1):
        count +=1
    begin = count
    while (horizontal_array[count] != 0) & (count != image.shape[1]-1):
        count +=1
    end = count
    if(count != image.shape[1]-1):
        characters.append([begin,end])

vertical_array = np.empty(image.shape[0], int)

for character in range(len(characters)):      
    for line in range(image.shape[0]):
        result = 0
        for pixel in range(characters[character][0], characters[character][1]):
            if(image[line,pixel] > 1):
                result = result + 1
        horizontal_array[line] = result   
    begin = 0
    end = 0
    count = 0
    while(count != image.shape[0]-1):
        while (horizontal_array[count] == 0) & (count != image.shape[0]-1):
            count +=1
        begin = count
        while(count != image.shape[0]-1):
            count +=1
            if(horizontal_array[count] > 1):
                end = count
    
    characters[character].append(begin)
    characters[character].append(end)
  
print(characters)  

for character in range(len(characters)):
    data = cv2.rectangle(data, (characters[character][0], characters[character][2]), (characters[character][1], characters[character][3]), (255,0,0), 1)
cv2.drawContours(data,contours,-1,(0,255,0),1)
while True:
    cv2.imshow('image', data)
        
    if cv2.waitKey(0)==27:    # Esc key to stop
        break    
cv2.destroyAllWindows()

