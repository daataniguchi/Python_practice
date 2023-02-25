import os
import shutil
import FocusStack


def stackHDRs(image_files, filename, path):
    print(image_files)
    focusimages = []
    for img in image_files:
        print("Reading in file {}".format(img))
        focusimages.append(cv2.imread(img))

    merged = FocusStack.focus_stack(focusimages)
    cv2.imwrite(os.path.join(path , filename), merged)
    return merged

def get_image_files(root_dir, img_types):
    #os.walk creates 3-tuple with (dirpath, dirnames, filenames)

    # Get all the root directories, subdirectories, and files
    full_paths = [x for x in os.walk(root_dir)]
    imgs_temp = [os.path.join(ds,f) for ds,_,fs in full_paths for f in fs if f]

    # Filter out so only have directories with .jpg, .tiff, .tif, .png, .jpeg
    imgs = [j for j in imgs_temp if any (k in j for k in img_types)]
    return imgs

root_dir =
img_types = '.tif'
files = get_image_files(root_dir, img_types)
channels = ['CH1', 'CH2', 'CH3', 'CH4']
range = (list(range(1, 31)))
range = [str(i).zfill(2) for i in range]
FF_folder_name = 'FF_images'
FF_folder_dir = os.path.join(root_dir, FF_folder_name)
isExist = os.path.exists(FF_folder_dir)
if not isExist:
    os.makedirs(FF_folder_dir)
    print('FF images folder created')
else:
    print('FF images folder already exists')
error = []
for x in channels:
    ch_images = [c for c in files if x in c]
    for i in range:
        position = 'position_' + i
        img_in_pos_per_ch = [c for c in ch_images if position in c]
        print('There are', len(img_in_pos_per_ch), x, 'images in position', i)
        path = os.path.join(FF_folder_dir, position)
        exist = os.path.exists(path)
        if not exist:
            os.makedirs(path)
        input = os.path.join(root_dir, 'temp')
        os.makedirs(input)
        for c in img_in_pos_per_ch:
            shutil.copy(c, input)
        image_files = get_image_files(input, img_types)
        filename = position + "_" + x + ".tif"

            img = stackHDRs(image_files, filename, path)
        except:
            ch_pos = x + '_' + position
            error.append(ch_pos)
            pass
        shutil.rmtree(input)
print('Done!')
print('The following positions could not be stacked:')
print(error)
