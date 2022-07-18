#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 19:12:53 2022

@author: gustavo
"""

import numpy as np
import os
import shutil

def read_dir():
    #save and move to the original dataset path
    print('changed to ' + str(os.getcwd()) + '/by_class \n')
    old_ds_path = str(os.getcwd() + '/by_class')
    os.chdir(old_ds_path)
    #make a list of all the character folders
    print('folders found:'+ str(os.listdir()) + '\n')
    old_folders = os.listdir()
    folders_dict = {}
    #create a new folder for the dataset
    os.chdir(str(os.getcwd())+'/..')
    print('changed to ' + str(os.getcwd()))
    new_ds_path = str(os.getcwd())+'/dataset_only_characters'
    os.makedirs(new_ds_path, exist_ok = True)
    os.chdir(new_ds_path)
    print('changed to ' + str(os.getcwd()))
    #create train and test folder
    train_path = new_ds_path + '/train'
    test_path = new_ds_path + '/test'
    os.makedirs(train_path, exist_ok = True)
    os.makedirs(test_path, exist_ok = True)
    #create new folders with respect to each character
    print('creating new folders...')
    os.chdir(train_path)
    char_old_folders = []
    for folder in old_folders:
        ascii_conversor = bytes.fromhex(folder)
        if(ascii_conversor.decode("ASCII") >= 'a'):
            folders_dict.update({str(folder): ascii_conversor.decode("ASCII")})
            os.makedirs(train_path + '/' +ascii_conversor.decode("ASCII"), exist_ok = True)
            char_old_folders.append(folder)
  
    new_folders = os.listdir() 
    print('folders created: '+ str(new_folders) + '\n')
    
    os.chdir(test_path)
    for folder in old_folders:
        ascii_conversor = bytes.fromhex(folder)
        if(ascii_conversor.decode("ASCII") >= 'a'):
            folders_dict.update({str(folder): ascii_conversor.decode("ASCII")})
            os.makedirs(test_path + '/' +ascii_conversor.decode("ASCII"), exist_ok = True)
        
    new_folders = os.listdir() 
    print('folders created: '+ str(new_folders) + '\n')

    # copy the images on the new folders
    for old_folder in char_old_folders:
        os.chdir(str(old_ds_path + '/' +old_folder))
        subfolders = os.listdir()
        for subfolder in subfolders:
            #copy the images of all the folders but one
            if((subfolder.startswith('hsf')) & (subfolder.endswith('.mit')==False) & (subfolder.endswith('7') == False)):
                os.chdir(str(old_ds_path + '/' +old_folder+ '/' +subfolder))
                images = os.listdir()
                for image in images:
                    shutil.copy(str(old_ds_path + '/' +old_folder+ '/' +subfolder+ '/' + image), str( train_path + '/' + folders_dict[old_folder]+ '/' + image))
            else:
                #saving a folder for test
                if(subfolder.endswith('7')):
                    os.chdir(str(old_ds_path + '/' +old_folder+ '/' +subfolder))
                    images = os.listdir()
                    for image in images:
                        shutil.copy(str(old_ds_path + '/' +old_folder+ '/' +subfolder+ '/' + image), str( test_path + '/' + folders_dict[old_folder]+ '/' + image))
  
read_dir()