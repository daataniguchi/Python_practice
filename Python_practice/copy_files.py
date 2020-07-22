#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 16:29:25 2020

@author: anissagarcia
"""

import os
import shutil
import os.path
src_dir = #"imput folder directory where you want files to be copied from"
src_files = [x for x in src_dir if x.endswith ('.jpg')]
src_files = (os.listdir(src_dir))
target_dir = #"imput folder directory where you want the files to be copied to"
def valid_path(dir_path, filename):
    full_path = os.path.join(dir_path, filename)
    return os.path.isfile(full_path)
files = [os.path.join(src_dir, f) for f in src_files if valid_path(src_dir, f)]
for f in range(0,#insert number of range):
    shutil.copy(files[f], target_dir)
    
print('Finished!')