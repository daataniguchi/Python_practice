Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:54:52) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> ##printing out the duplicate folders in each category

import os

file_path_ciliates = '/Users/keomonydiep/Desktop/training_images/ciliates' ##path to the image files
file_list_ciliates = os.listdir(file_path_ciliates) ##store image files in a list 
#print(file_list_ciliates) ##print out the list of image files 

for file in file_list_ciliates: ##for item/element in file_list_ciliates
    if file.endswith('copy.jpg'): ##if the item/element ends with 'copy.jpg' (duplicate)
        print(file) #print that out 
        
file_path_l_poly = '/Users/keomonydiep/Desktop/training_images/l_poly/'
file_list_l_poly = os.listdir(file_path_l_poly)
#print(file_list_l_poly)

for file in file_list_l_poly:
    if file.endswith('copy.jpg'):
        print(file)

        
file_path_other = '/Users/keomonydiep/Desktop/training_images/other/'
file_list_other = os.listdir(file_path_other)
#print(file_list_other)

for file in file_list_other:
    if file.endswith('copy.jpg'):
        print(file)
        
SyntaxError: multiple statements found while compiling a single statement
>>> 
