#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:52:05 2022

@author: gustavo
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
img_width, img_height = 128,128
num_classes = 62
train_path = '/home/gustavo/OCR_project/python/new_dataset/train'
test_path = '/home/gustavo/OCR_project/python/new_dataset/test'

train_ds = tf.keras.utils.image_dataset_from_directory(
    train_path,
    labels='inferred',
    label_mode='categorical',
    color_mode='grayscale',
    batch_size=32,
    image_size=(img_width, img_height),
    shuffle=True,
    seed=None,
    validation_split=None,
    subset=None,
    interpolation='bilinear',
    follow_links=False,
    crop_to_aspect_ratio=False,
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    test_path,
    labels='inferred',
    label_mode='categorical',
    color_mode='grayscale',
    batch_size=32,
    image_size=(img_width, img_height),
    shuffle=True,
    seed=None,
    validation_split=None,
    subset=None,
    interpolation='bilinear',
    follow_links=False,
    crop_to_aspect_ratio=False,
)

"""
normalization_layer = layers.Rescaling(1./255)
norm_ds_train= train_ds.map(lambda x, y: (normalization_layer(x), y))
norm_ds_test = test_ds.map(lambda x, y: (normalization_layer(x), y))
"""

norm_ds_train= train_ds
norm_ds_test = test_ds

cnn = tf.keras.models.Sequential()
cnn.add(layers.Rescaling(1./255))
cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=11, activation='relu', input_shape=[img_width, img_height, 1]))
cnn.add(tf.keras.layers.MaxPooling2D(pool_size=2, strides=2))
cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=11, activation='relu'))
cnn.add(tf.keras.layers.MaxPooling2D(pool_size=2, strides=2))
cnn.add(tf.keras.layers.Flatten())
cnn.add(tf.keras.layers.Dense(units=64, activation='relu'))
cnn.add(tf.keras.layers.Dense(num_classes, activation = 'softmax'))
cnn.compile(optimizer = 'adam', loss=tf.keras.losses.CategoricalCrossentropy(), metrics = ['accuracy'])
callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
cnn.fit(x = norm_ds_train, validation_data = norm_ds_test, epochs = 20)
cnn.save('ocr_model.h5')