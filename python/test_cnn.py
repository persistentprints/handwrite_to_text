#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 21:07:16 2022

@author: gustavo
"""

import numpy as np
from numpy import set_printoptions
import tensorflow as tf
from keras.utils import load_img
from keras.utils import img_to_array
model = tf.keras.models.load_model('/home/gustavo/OCR_project/python/models/mnist_model.h5')
test_image = load_img('/home/gustavo/4.png', target_size = (28, 28),color_mode='grayscale',)
test_image = img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
#test_image = test_image/255.0
classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
result = model.predict(test_image)
set_printoptions(suppress=True, precision=4)
print(result)
index = (np.argmax(result).astype(int))
print(classes[index])
