#Program created by Brooke Wright & Sandra Morcos
#Edited By Jose Tapia
# importing the module -- always put importing things at the top of the code
import ast
import random 
import os
import shutil

# reading the data from the file
with open(r"C:\Users\Pepep\Documents\Palomar\BridgesScholar\Research\AndreaTest\classification_file_names_04_17_023.txt") as f:
    data = f.read()
    f.close()

# reconstructing the data as a dictionary
data_dict = ast.literal_eval(data)

# determine how many random values you want from each value in the dictionary
num_rand = 25

# go through the dictionary and take a random sample from each value
r = {}

for k,v in data_dict.items():
    r[k] = []
    for i in v:
        i = os.path.basename(i)
        r[k].append(i)

for k, v in r.items():
    r[k] = random.sample(v,num_rand)

        

#Creat a new dictionary for the random values
#for k, v in data_dict.items():
 

#r[k] = random.sample(i,num_rand)

f = open(r'C:\Users\Pepep\Documents\Palomar\BridgesScholar\Research\AndreaTest\txtfilerand_out.txt', "w")
f.write(str(r))
f.close()


#Directory set up
#Access the test set directory 
test_dir = r'C:\Users\Pepep\Documents\Palomar\BridgesScholar\Research\AndreaTest\2020-04-17_063700_2020-04-18_063700'
#Creates a list of all image names inside the original test set.
files = os.listdir(test_dir)
#Creates the directory in which the randomized images will be organized
rand_dir = r'C:\Users\Pepep\Documents\Palomar\BridgesScholar\Research\AndreaTest\random_img'


#Read in the dictionary textfile
randImg = open(r"C:\Users\Pepep\Documents\Palomar\BridgesScholar\Research\AndreaTest\txtfilerand_out.txt", "r")
randData = randImg.read()
randImg.close() 

#Creates dictionaries from randData 
rand_dict = ast.literal_eval(randData)

#Creates directory using the key names of given textfile as folders, all within one main folder

#Access the dictionary created with rand_dict. k=keys, v = values
for k,v in rand_dict.items():
    #Create the specific Ciliate,L_poly, and Other folders within the random directory created above
    #This will look lie \2020_02_06_Test\RandomImages\Ciliate 
    dir_name = os.path.join(rand_dir, k)
    #checks to see if the paths exists, if they don't then it'll make it
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    #Checks to see if the randomly chosen images are in the original test directory
    for i in files:
        #if it exists, copy from the test directory to the newly created RandomImages paths
        if i in v:
            shutil.copy(os.path.join(test_dir,i), os.path.join(dir_name,i))

outputs= r'C:\Users\Pepep\Documents\Palomar\BridgesScholar\Research\AndreaTest\RandomDump'
#use rand_dir from above because it is contains the random images, but organized.
#use os.walk() to access the organized director
for path,dirs,files in os.walk(rand_dir):
    if not os.path.exists(outputs):
        os.makedirs(outputs)
    #print(files)
    for f in files:
        #Use join to combine the name of the image to the original path
        #Join on the left grabs the image to then be moved and "dumped" into a new RandomDump folder to then be used for the GUI
        shutil.copy(os.path.join(path,f), os.path.join(outputs, f))

