
import os
import shutil

path_1 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_1_computer/Ciliate_guest1/' 
path_2 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_3_computer/Ciliate_guest3/'
path_3 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_1_computer/Lingulodinium_polyedra_guest1/'
path_4 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_3_computer/Lingulodinium_polyedra_guest3/'
path_5 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_1_computer/Other_guest1/'
path_6 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_3_computer/Other_guest3/'
path_7 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_1_computer/Questionable_guest1/'
path_8 = '/Users/yulismamartinez/Desktop/Python_practice/Master_images_guest_3_computer/Questionable_guest3/'

path_9 = '/Users/yulismamartinez/Desktop/Python_practice/Final_Images/Ciliate/'#moving Ciliate images here
path_10 = '/Users/yulismamartinez/Desktop/Python_practice/Final_Images/Lingulodinium_polyedra/'
path_11 = '/Users/yulismamartinez/Desktop/Python_practice/Final_Images/Other/'
path_12 = '/Users/yulismamartinez/Desktop/Python_practice/Final_Images/Questionable/'

source1 = path_1
source2 = path_2
destination = path_9

a = os.listdir(source1) #adjust the "path_1/2" to the paths you want to use
b = os.listdir(source2)

if a == b:
    print("folders contain the same images")
elif a != b:
    print("folders do not contain the same images")

    dif_files_path1 = [x for x in a if x not in b] #this will only look at the images that are in A but not in B
    for i in dif_files_path1:
        shutil.move (source1+i, destination+i) 

    dif_files_path2 = [x for x in b if x not in a] #this will only look at the images that are in B but not in A
    for i in dif_files_path2:
        shutil.move (source2+i, destination+i) 


    same_files = [x for x in a if x in b]
    for i in same_files:
        shutil.move (source1+i, destination+i)