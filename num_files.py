#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 22:46:10 2020

@author: anissagarcia
"""

import os
from pathlib import Path
        
path = "/dir/path/"
categories = ["#insert catergory name(s)"]

file_list = []
file_num = []

for r, d, f in os.walk(path):
    if r.split('/'[-1]) == categories:
        num_files = len(f)
        file_list.append(f)
        file_num.append(num_files)
        num_files.append(r, d, f)
        file_count = sum(len(f) for _, _, files in os.walk(path))
        
    print('r', r)
    print('d', d)
    print('f', f)
    print('Total: ', len(f))

print('Overall Total: ', file_count-1) #-1 is added to exclude the hidden folder