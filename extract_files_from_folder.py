Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:54:52) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> import os

def func_2():
    path = '/Users/keomonydiep/Desktop/training_images/ciliates/'##path to the ciliate image files
    a = os.listdir(path) ##retrieve image files using os.listdir()
    print(a[:4]) ##print out the first four images within the list
    print('length of images in ciliates is ' + str(len(a))) ##print out the length of files in the ciliates

    path_2 = '/Users/keomonydiep/Desktop/training_images/l_poly/' ##path to l_poly image files
    b = os.listdir(path_2)##retrieve image files
    print(b[:4])##print out the first four images within the list
    print('length of images in l_poly is ' + str(len(b))) #print out length of files in l_poly

    path_3 = '/Users/keomonydiep/Desktop/training_images/other/' ##path to other image files
    c = os.listdir(path_3) ##retrieve image files
    print(c[:4]) ##print out the first four images within the list
    print('length of images in other is ' + str(len(c))) #print out length of files in other

func_2()
