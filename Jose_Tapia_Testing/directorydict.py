# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 00:29:47 2021

@author: Jose Tapia, Alyssia Gonzalez, Yulisma

@Program: Create a dictionary using a directory path. Folder values will be keys and their respective contents are the values.
"""

import os
import fnmatch
from collections import defaultdict

#defaultdict(list) creates a dictionary that has lists as values, emphasis on "list"

d = defaultdict(list) 

#Uses folder names as keys and the respective contents as their values. 

for path,dirs,files in os.walk(r'C:\Users\Pepep\Documents\Palomar\BridgesScholar\Research\2020_02_06_Test\TestOutput'):
   for f in fnmatch.filter(files,'*.jpg'):

      d[os.path.basename(path)].append(f)
     
      
#Reassign d and pass the defaultdict into a regular dictionary, using dict()     
d = dict(d)      
print(d)
#The directory should lead to your most efficient spot, in this case I put it in my overall test folder.
f = open(r"C:\Users\Pepep\Documents\Palomar\BridgesScholar\Research\2020_02_06_Test\classification_names_2020_02_06_Test.txt", "w")
f.write(str(d))
f.close
#print(dict(d))


