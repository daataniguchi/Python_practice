#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 14:38:07 2020

@author: yulismamartinez
"""

#########code works to create directories of category ##############
#########and then copy what is in those folders into their folder###


import os
import shutil
def copy_image_files(root_dir, img_types,destination):
   #os.walk creates 3-tuple with (dirpath, dirnames, filenames)
   # Get all the root directories, subdirectories, and files
    full_paths = [x for x in os.walk(root_dir)]
    imgs_temp = [os.path.join(ds,f) for ds,_,fs in full_paths for f in fs if f] 
   # Filter out so only have directories with .jpg, .tiff, .tif, .png, .jpeg
    imgs = [j for j in imgs_temp if any (k in j for k in img_types)]
    categories_in_folders= {x.split('/')[-2] for x in imgs}#curly brackets makes them into a set
    
    for m in categories_in_folders:
        if not os.path.exists(destination+m):
            os.makedirs(destination+m)

    for l in imgs:
        category=l.split('/')[-2]
        shutil.copy(l,destination+category)

dest='/Users/yulismamartinez/Desktop/Research/Labeled_data_part_3/Part_3_2019_Labeled_Images/'
p= copy_image_files(root_dir='/Users/yulismamartinez/Desktop/Research/Labeled_data_part_3/SPCP2_unlabeled_data_part_3/', img_types=['.jpg'], destination=dest)
