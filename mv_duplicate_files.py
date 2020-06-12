import os
import shutil

def mv_duplicate_files(source1, source2, destination,file_types):
    
    # This function compares files in source1 and source2 and moves duplicate files 
        #so destination directory has single set of each file
        
    # source1 is one directory want to compare files in
    # source2 is other directory want to compare files in
    # destination is where complete set of non-duplicate files will end up
    # file_types are the types of files want moved to destination directory
    
    files1 = os.listdir(source1) 
    files2 = os.listdir(source2)
    files3 = os.listdir(destination)


    if files1 == files2:
        print("directories contain the same files")

    elif files1 != files2:
        print("directories do not contain the same files")

        #Only look at the images in files1 but not in files2
        dif_files_temp = [x for x in files1 if x not in files2] 
        
        # Only dealing with file types of interest
        dif_files_1_temp = [j for j in dif_files_temp if any (k in j for k in file_types)]
        
        #Ensure files in source1 not already in destination folder
        dif_files_1 = [x for x in dif_files_1_temp if x not in files3]
        for i in dif_files_1:
            shutil.move (source1+i, destination+i) 
   
        #Only look at the images that are in files2 but not in files1
        dif_files_temp = [x for x in files2 if x not in files1] 
        dif_files_2_temp = [j for j in dif_files_temp if any (k in j for k in file_types)]
        dif_files_2 = [x for x in dif_files_2_temp if x not in files3]
        for i in dif_files_2:
            shutil.move (source2+i, destination+i) 
        
        # Move images that are same in both folders
        same_files_temp = [x for x in files1 if x in files2]
        same_files = [j for j in same_files_temp if any (k in j for k in file_types)]
        for i in same_files:
            shutil.move (source1+i, destination+i)


# Specify directories want to compare and where want files to end up   
path_groups = [('/Users/dtaniguchi/Desktop/Test_images/Ciliate1/',#folder_1 for comparison
                '/Users/dtaniguchi/Desktop/Test_images/Ciliate2/',#folder_2 for comparison
                '/Users/dtaniguchi/Desktop/Test_images/Ciliate_Final/' ),#destination for files
                ('/Users/dtaniguchi/Desktop/Test_images/Lpoly1/',#folder_1 for comparison
                '/Users/dtaniguchi/Desktop/Test_images/Lpoly2/',#folder_2 for comparison
                '/Users/dtaniguchi/Desktop/Test_images/Lpoly_Final/' )]#destination

# Specify file types want to look at actually move around
file_types = ('jpg')

# Run function
for paths in path_groups:
    mv_duplicate_files(paths[0],paths[1],paths[2],file_types)