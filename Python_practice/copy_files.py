#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 16:29:25 2020

@author: anissagarcia
"""

import os #will give us the exact location of execution
import shutil #resposible for copying files and directories
import random #generates random #s
import os.path #path module. This is used to work with the files with a given path

src_dir = '/Users/anissagarcia/Desktop/Research_2020/python_practice_dogs/shih_tzu_1' #folder you want files to be copied
target_dir = '/Users/anissagarcia/Desktop/Research_2020/python_practice_dogs/shih_tzu_1/test' #new folder where you want your copies to be copied to
src_files = (os.listdir(src_dir)) #src defines the directory by giving the names of the files and what folder they are located in; give me the list of the files

def valid_path(dir_path, filename): #defining the path you want the copies to be found
    full_path = os.path.join(dir_path, filename) #reiterating the above step
    return os.path.isfile(full_path) #give me the full path of where the files were copied to

files = [os.path.join(src_dir, f) for f in src_files if valid_path(src_dir, f)] #copying files from src_dir to target_dir
choices = random.sample(files, 6) #Getting n files. Change the number according to folder size
for files in choices:
    shutil.copy(files, target_dir) #Move files from src_dir to target_dir

print('Finished!')