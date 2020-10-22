#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 22:46:10 2020

@author: anissagarcia
"""

import os
from pathlib import Path

path = "dir"
categories = ["imput", "each", "category"]


file_list = []
#file_num = []


for r, d, f in os.walk("dir"): #walk throgh the path that was given
    if r.split('/'[-1]) == categories: #Go through each category that was given to look through; focus on everything that is after /
        num_files = len(f)+num_files #give me the total number of files in each folder
        file_list.append(f) #append will add the name of the file to the end of the list
        file_num.append(num_files) 
                    
             
    print('r', r) #within the loop, give me the name of the root dir. 
    print('d', d) #within the loop, give me the name of the dir
    print('f', f) #within the loop, give me the name of the file
    print('Total: ', len(f)) #within the loop, give me total number of files in each subdirectory

    
total_count = sum(len(files) for _, _, files in os.walk(r'dir')) #go through all of the folders and subfolders
print('Overall Total: ', total_count) #give me the total of files that are found in this folder.
   

   