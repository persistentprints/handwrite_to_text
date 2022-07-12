#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 20:49:26 2022

@author: gustavo
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.text import FontContextManager as FCM
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.graphics import Line
     
    
class loadScreen(Screen):
    pass
class appScreen(Screen):
    def __init__(self, **kwargs):
        super(appScreen, self).__init__(**kwargs)
        self.painter = drawWidget()
        self.children[0].add_widget(self.painter)
        
    def process(self):
        self.painter.process()
    
    def clear(self):
        self.painter.clear()

class drawWidget(Widget):
    def on_touch_down(self, touch):
        print("touched" + str(touch.pos))
        with self.canvas:
            Color(0,0,0,1, mode="rgba")   
            self.line = Line(points=[touch.pos[0], touch.pos[1]], width=2)
        
    def on_touch_move(self, touch):
        self.line.points = self.line.points + [touch.pos[0], touch.pos[1]]
        
    def clear(self):
        self.canvas.clear()
        print('cleared')
    
    def process(self):
        self.export_to_png("img.png")
        
class mainApp(App):
    def build(self):
        self.screenManager = ScreenManager()
        self.screenManager.add_widget(loadScreen(name='load'))
        self.screenManager.add_widget(appScreen(name='app'))
        Clock.schedule_once(self.animation_callback, 3)
        return self.screenManager
    def animation_callback(self,dt):
        self.screenManager.current = 'app'
        
app = mainApp()
app.run()