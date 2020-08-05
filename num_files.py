#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 22:46:10 2020

@author: anissagarcia
"""

import os
##################################################
####### Below will give you the file count #######
##################################################

#list = os.listdir("folder/directory")
#number_files = len(list)

#print (number_files)

#################################################
##### Below willl give you a list of the folder and the subdirectories######
#################################################

import os
path = "/Users/anissagarcia/Desktop/Research_2020/Anissa_classified_images/SPCP2_unlabeled_data_part_3"
categories = ['Ciliate', 'L.poly', 'Questionable', 'Other']
#subdirs = [x[0] for x in os.walk(path)]

#files = []
for r, d, f in os.walk(path):
    print('r', r)
    print('d', d)
    print('f', f)
#    for file in f:
 #       files.append(os.path.join(r, file))
#for f in files:
 #   print(f)
#print(subdirs)