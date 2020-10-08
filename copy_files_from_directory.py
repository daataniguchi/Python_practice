# Copy images from subfolders to different directory

# Use this code to copy files from subfolders 
# to a different destination directory

import os
import shutil
def copy_files(src_dir, file_types,dest_dir):
# src_dir is the directory which contains subfolders in fromwhich want to extract files
# file_types = files of a particular type (e.g., jpeg, docx) that want to focus on 
# dest_dir = directory in which will create subfolders and copy images from src_dir

    full_paths = [x for x in os.walk(src_dir)]
    file_temp = [os.path.join(ds,f) for ds,_,fs in full_paths for f in fs if f] 
    files = [j for j in file_temp if any (k in j for k in file_types)]
    categories_in_folders= {x.split('/')[-2] for x in files}
    categories_in_folders = [x for x in categories_in_folders if not x.startswith('20')] #subdirs begin with year, which are all in the 2000s
    for m in categories_in_folders:
        if not os.path.exists(dest_dir+m):
            os.makedirs(dest_dir+m)
    for l in files:
        category=l.split('/')[-2]
        if not category.startswith('20'):
            shutil.copy(l,dest_dir+category)
        # shutil.copy(l,dest_dir+category)

        
        
src = '/Users/dtaniguchi/Research/SPCS_images/Images_downloaded_2020_classified/SPCP2_labeled_data_part_2/'        
dest='/Users/dtaniguchi/Research/SPCS_images/Images_downloaded_2020_classified_and_combined/SPCP2_labeled_data_part_2/'

copy_files(src_dir = src, file_types=['.jpg'], dest_dir=dest)