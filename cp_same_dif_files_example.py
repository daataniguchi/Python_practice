import os
import shutil

def cp_same_dif_files(source1, source2, destination_same, destination_dif,file_types):
    
    # This function compares files in source1 and source2 and copies duplicate (same) files 
        #so destination_same directory has files that are the same in source1 and source2
        # while destination_dif has subdirectories of files that are the different in the two sources
        
    # source1 is one directory want to compare files in
    # source2 is other directory want to compare files in
    # destination_same is where complete set of non-duplicate, same files will end up
    # destination_dif is where the files that are different between sources will end up, 
        # in destination_dif/source1 and destination_dif/source2 specifically
    # file_types are the types of files want moved to destination directory
    
    files1 = os.listdir(source1) 
    files2 = os.listdir(source2)
    files3 = os.listdir(destination_same)

    if not os.path.isdir(destination_dif+'/source1'):
        os.makedirs(destination_dif+'/source1')
    if not os.path.isdir(destination_dif+'/source2'):
        os.makedirs(destination_dif+'/source2')
        
    files4 = os.listdir(destination_dif)

    if files1 == files2:
        print("directories contain the same files; no files copied; focus on one of source directories")

    elif files1 != files2:
        print("directories do not contain the same files")

        #Only look at the images in files1 but not in files2
        dif_files_temp = [x for x in files1 if x not in files2] 
        
        # Only dealing with file types of interest
        dif_files_1_temp = [j for j in dif_files_temp if any (k in j for k in file_types)]
        
        #Ensure files in source1 not already in destination folder
        dif_files_1 = [x for x in dif_files_1_temp if x not in files4]
        
        #Copy files only found in files1 into destination_dif1
        for i in dif_files_1:
            shutil.copy2 (source1+i, destination_dif+'/source1/'+i) 
   
        #Only look at the images that are in files2 but not in files1
        dif_files_temp = [x for x in files2 if x not in files1] 
        dif_files_2_temp = [j for j in dif_files_temp if any (k in j for k in file_types)]
        dif_files_2 = [x for x in dif_files_2_temp if x not in files4]
        for i in dif_files_2:
            shutil.copy2 (source2+i, destination_dif+'/source2/'+i) 
        
        # Move images that are same in both folders
        same_files_temp = [x for x in files1 if x in files2]
        same_files_temp_2 = [j for j in same_files_temp if any (k in j for k in file_types)]
        same_files = [x for x in same_files_temp_2 if x not in files3]
        for i in same_files:
            shutil.copy2 (source1+i, destination_same+i)


# Specify directories want to compare and where want files to end up   
# Note the structure of this list path_groups. This structure is chosen so it can
# be inptu into a for loop at the end of this script
path_groups = [['/Users/dtaniguchi/Desktop/Test_images/Ciliate1/',#folder_1 for comparison
                '/Users/dtaniguchi/Desktop/Test_images/Ciliate2/',#folder_2 for comparison
                '/Users/dtaniguchi/Desktop/Test_images/Ciliate_Final/',#destination for files that are the same
                '/Users/dtaniguchi/Desktop/Test_images/ciliate_dif'],#destination for files that are the different
                ['/Users/dtaniguchi/Desktop/Test_images/Lpoly1/',#folder_1 for comparison
                '/Users/dtaniguchi/Desktop/Test_images/Lpoly2/',#folder_2 for comparison
                '/Users/dtaniguchi/Desktop/Test_images/Lpoly_Final/',#destination for same
                '/Users/dtaniguchi/Desktop/Test_images/Lpoly_dif']] #destination different

# Specify file types want to look at actually move around
file_types = ['jpg']

# Run function in a for loop (hence the structure of the list path_groups above)
for paths in path_groups:
    cp_same_dif_files(paths[0],paths[1],paths[2],paths[3],file_types)
