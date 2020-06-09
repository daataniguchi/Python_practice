
import os
import shutil

path_1 = '/Users/yulismamartinez/Desktop/Ciliates_guest1N' 
path_2 = '/Users/yulismamartinez/Desktop/Ciliates_guest3'
path_3 = '/Users/yulismamartinez/Desktop/Lpoly_guest1'
path_4 = '/Users/yulismamartinez/Desktop/Lpoly_guest3'
path_5 = '/Users/yulismamartinez/Desktop/Different_Ciliate_Images'# this is where we will be moving the images to
path_6 = '/Users/yulismamartinez/Desktop/Different_Lpoly_Images'

a = os.listdir(path_1) #adjust the "path_1/2" to the paths you want to use
b = os.listdir(path_2)


if a == b:
    print("folders contain the same images")
elif a != b:
    print("folders do not contain the same images")

dif_files_path1 = [x for x in a if x not in b] #this will only look at the images that are in A but not in B
for i in dif_files_path1:
    source = '/Users/yulismamartinez/Desktop/Ciliates_guest1N/'
    destination = '/Users/yulismamartinez/Desktop/Different_Ciliate_Images/'
    shutil.move (source+i, destination+i) 
print (path_1)
print ("files found only in Ciliates_guest1:")
print(dif_files_path1)


dif_files_path2 = [x for x in b if x not in a] #this will only look at the images that are in B but not in A
for i in dif_files_path2:
    source = '/Users/yulismamartinez/Desktop/Ciliates_guest3/'
    destination = '/Users/yulismamartinez/Desktop/Different_Ciliate_Images/'
    shutil.move (source+i, destination+i) 
print (path_2)
print ("files found only in Ciliates_guest3:")
print(dif_files_path2)


same_files = [x for x in a if x in b]
for i in same_files:
    source = '/Users/yulismamartinez/Desktop/Ciliates_guest1N/'
    destination = '/Users/yulismamartinez/Desktop/Different_Ciliate_Images/'
    shutil.move (source+i, destination+i)
print ("files that are the same:")
print(same_files)


#i think that we can comment out some print statments now