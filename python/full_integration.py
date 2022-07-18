#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 18:47:12 2022

@author: gustavo
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.graphics import Line
import cv2
import numpy as np     
from numpy import set_printoptions
import tensorflow as tf
from keras.utils import load_img
from keras.utils import img_to_array

line_width = 6
class procesor():
    def __init__(self, name, proportion = None, roi_area = None):
        self.canvas_size = 128
        self.name = name # name as a string with the file type ex'.png'
        self.roi_area = roi_area #region of interest as a list begining with the x position and then the y position
        self.model = tf.keras.models.load_model('/home/gustavo/OCR_project/python/models/char_ocr_model_128_v1.h5')
        #self.classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.classes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        if(proportion == None):
            self.pixel_proportion = int((self.canvas_size * (2/5)))
        else:
            self.pixel_proportion = int((self.canvas_size * proportion))
        
    def load(self):
        print("ok")
        while True:
            try:
                self.load = cv2.imread(self.name, cv2.IMREAD_UNCHANGED)
                break
            except:
                print("could not load image")
            
        if(self.roi_area == None):
            self.roi = self.load
        else:
            self.roi = self.load[self.roi[2]:self.roi[3],self.roi[0]:self.roi[1]]
        self.image_inv = self.roi[:,:,3]
        self.image = (255-self.image_inv)
        self.shape_x = self.image_inv.shape[1]
        self.shape_y = self.image_inv.shape[0]
    
    def detect(self):
        #create an array containing all the white pixels of each vertical array of the inverted image
        #this will hellp to detect the characters in the horizontal axis
        self.horizontal_array = np.empty(self.shape_x, int)
        #move to each horizontal position of the image to apply the sum of the white pixels of the image
        for line in range(self.shape_x):
            result = 0
            #sum each pixel of an horizontal line
            for pixel in range(self.shape_y):
                if(self.image_inv[pixel,line] > 1):
                    result = result + 1
            #assing the result to the corresponding postion of the horizontal_array
            self.horizontal_array[line] = result  
        
        #detect the characters with the previously calculated horizontal_array and save their position
        count = 0   
        self.characters = [] 
        while count != self.shape_x -1: # iterate until the count reaches the image shape
            while (self.horizontal_array[count] == 0) & (count != self.shape_x -1):
                count +=1 
            begin = count #detect when the array is not 0, that means that the count found a character
            while (self.horizontal_array[count] != 0) & (count != self.shape_x -1):
                count +=1 #detect when the array is 0, that means the cound found the end of a character
            end = count
            if(count != self.shape_x -1):
                self.characters.append([begin,end])
                
        
        #create a vertical array that detects the vertical position of each character
        #using the horizontal positions previously calculated
        self.vertical_array = np.empty(self.shape_y, int)

        for character in range(len(self.characters)):      
            for line in range(self.shape_y):
                result = 0
                for pixel in range(self.characters[character][0], self.characters[character][1]):
                    if(self.image_inv[line,pixel] > 1):
                        result = result + 1
                self.horizontal_array[line] = result   
            begin = 0
            end = 0
            count = 0
            while(count != self.shape_y-1):
                while (self.horizontal_array[count] == 0) & (count != self.shape_y-1):
                    count +=1
                begin = count
                while(count != self.shape_y-1):
                    count +=1
                    if(self.horizontal_array[count] > 1):
                        end = count
            
            self.characters[character].append(begin)
            self.characters[character].append(end)
        print(str(len(self.characters)) + " characters detected")
            
    def pack(self):
        #resize and save each character into a 128x128 image for later clasification
        self.character_imgs = []
        for character in range(len(self.characters)):
            character_img = np.zeros((self.canvas_size, self.canvas_size), dtype=np.uint8)
            character_img.fill(255) #fill the image with blanck color
            size_x = self.characters[character][1] - self.characters[character][0]
            size_y = self.characters[character][3] - self.characters[character][2]
            aspect_ratio = size_y/size_x
            character_roi = self.image[self.characters[character][2]:self.characters[character][3], self.characters[character][0]:self.characters[character][1]]
            #check wich axis of the character is the longest and resize with respect that info
            if(aspect_ratio > 1):
                resized = cv2.resize(character_roi,(int(self.pixel_proportion/aspect_ratio), self.pixel_proportion), cv2.INTER_NEAREST)
            else:
                resized = cv2.resize(character_roi,(self.pixel_proportion , int(self.pixel_proportion * aspect_ratio)), cv2.INTER_NEAREST)
                
            #put the character in the middle of the empty image
            character_img[int((self.canvas_size-(resized.shape[0]))/2):int(((self.canvas_size-resized.shape[0])/2)+resized.shape[0]),int((self.canvas_size-(resized.shape[1]))/2):int(((self.canvas_size-resized.shape[1])/2)+resized.shape[1])] = resized
            #_,character_img  = cv2.threshold(character_img,64,255,cv2.THRESH_BINARY)
            cv2.imwrite((str(character) + '.png'), character_img)
            character_img = np.expand_dims(character_img, axis = 0)
            character_img = np.expand_dims(character_img, axis = 3)
            self.character_imgs.append(character_img)
            print(character_img.shape)
            
            
    def classify(self):
        results = ""
        for character in range(len(self.characters)):
            result = self.model.predict(self.character_imgs[character])
            set_printoptions(suppress=True, precision=4)
            index = (np.argmax(result).astype(int))
            results += self.classes[index]
        print(results)
        return results

# init screen
class loadScreen(Screen):
    pass

# main screen class
class appScreen(Screen):
    def __init__(self, **kwargs):
        super(appScreen, self).__init__(**kwargs)
        self.painter = drawWidget()
        self.children[0].add_widget(self.painter)
        
        
    def process(self):
        self.procesor = procesor("img.png")
        self.painter.process()
        self.procesor.load()
        self.procesor.detect()
        self.procesor.pack()
        text = self.procesor.classify()
        self.ids.process.text = str(text)

    def clear(self):
        self.painter.clear()
        
# drawing widget
class drawWidget(Widget):
    def on_touch_down(self, touch):
        #print("touched" + str(touch.pos))
        #detect when touched and start drawing
        with self.canvas:
            Color(0,0,0,1, mode="rgba")   
            self.line = Line(points=[touch.pos[0], touch.pos[1]], width=line_width)
            
    def on_touch_move(self, touch):
        # keep drawing on touch move
        self.line.points = self.line.points + [touch.pos[0], touch.pos[1]]
     
    #clear canvas    
    def clear(self):
        self.canvas.clear()
        print('cleared')
    #save and process image for character detection and clasification
    def process(self):
        self.export_to_png("img.png")
        
 #class main class for the GUI       
class mainApp(App):
    def build(self): 
        # add the different screens of the app
        self.screenManager = ScreenManager()
        self.screenManager.add_widget(loadScreen(name='load'))
        self.screenManager.add_widget(appScreen(name='app'))
        Clock.schedule_once(self.animation_callback, 3)
        return self.screenManager
    def animation_callback(self,dt):
        self.screenManager.current = 'app'
        
app = mainApp()
app.run()