
import os
import shutil

path_1 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_1_computer/Ciliate_guest1' 
path_2 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_3_computer/Ciliate_guest3'
path_3 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_1_computer/Lingulodinium_polyedra_guest1'
path_4 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_3_computer/Lingulodinium_polyedra_guest3'
path_5 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_1_computer/Other_guest1'
path_6 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_3_computer/Other_guest3'
path_7 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_1_computer/Questionable_guest1'
path_8 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_3_computer/Questionable_guest3'

path_9 = '/Users/yulismamartinez/Desktop/Python_practice/Final_Ciliate_Images'#moving Ciliate images here
path_10 = '/Users/yulismamartinez/Desktop/Python_practice/Final_Lingulodinium_polyedra_Images'
path_11 = '/Users/yulismamartinez/Desktop/Python_practice/Final_Other_Images'
path_12 = '/Users/yulismamartinez/Desktop/Python_practice/Final_Questionable_Images'

a = os.listdir(path_1) #adjust the "path_1/2" to the paths you want to use
b = os.listdir(path_2)

if a == b:
    print("folders contain the same images")
elif a != b:
    print("folders do not contain the same images")

dif_files_path1 = [x for x in a if x not in b] #this will only look at the images that are in A but not in B
source = path_1
destination = path_9
for i in dif_files_path1:
    #shutil.move (source+i, destination+i) 

dif_files_path2 = [x for x in b if x not in a] #this will only look at the images that are in B but not in A
source = path_2
destination = path_9
for i in dif_files_path2:
    #shutil.move (source+i, destination+i) 

