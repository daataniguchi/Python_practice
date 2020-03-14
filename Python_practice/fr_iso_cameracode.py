import numpy as np
from PIL import Image

#Frame Rate Loop

fps_top=30                                              #fps_top is the max(top) frame rate limit
fps_bottom=15                                           #fps_bottom is the min(bottom) frame rate limit
fps_increment=10                                        #fps_increment is the increment value
fps_lst=[fps_bottom]                                    #fps_lst the list in which frame rates will go, starting with the lower limit


#While loop:
while fps_bottom < fps_top:                             #Conditions set for the while loop: while top limit < bottom limit
    fps_bottom=fps_bottom+fps_increment                 # addition of fps_increment + fps_bottom= fps_bottom
    fps_lst.append(fps_bottom)                          # appending the new fps_bottom value to fps_lst
    
#if loop was added to avoid any number greater than top limit from being included in the list
#regardless of the increments
if fps_lst[len(fps_lst)-1] > fps_top:                   #If the last number is greater than the top limit
    fps_lst.pop()                                       #Then it will be popped out (won't be included
                                                        #in final list)
    
#print(fps_lst)


#ISO Loop

iso_top=800                                             #iso_top is the max(top) iso limit
iso_bottom=100                                          #iso_bottom is the min(bottom) iso limit
iso_increment=200                                       #iso_increment is the increment value
iso_lst=[iso_bottom]                                    #iso_lst the list in which ISO values will go, starting with the lower limit


#While loop to cycle though increment values
while iso_bottom < iso_top:                             # Conditions for the while loop: while the iso bottom limit is < iso top limit
    iso_bottom=iso_bottom+iso_increment                 # add iso_bottom and increments to replace iso_bottom valeu (Adding itself + increment)
    iso_lst.append(iso_bottom)                          # append the new iso_bottom value to iso_lst
    
# If loop added to avoid any number greater than top limit from being included in the list regardless of increments
if iso_lst[len(iso_lst)-1] > iso_top:                   # if the last number is greater than top limit it will be popped out
    iso_lst.pop()                                       # and it won't be included in final list
    
#print(iso_lst)

#Combinding both lists to get all possible permutations
#Total of permutations saved on total_per
combo=[]
total_per=0
#For loop:
for a in fps_lst:              #for a variable (a) in list 1
    for b in iso_lst:          #for a variable (b) in list 2
        combo.append([a,b])    #append variables a and b into list called combo
        total_per=total_per+1
        
#Making an array called permu_array and placing it in a list       
permu_array=np.array(combo)
#permu_array=combo
#print('Total of FR and ISO permutations: '+str(total_per))
#print(permu_array)


#Extracting one set of conditions and inserting X(FR) and Y(ISO) values into image name

#Image naming using while loop   
#i=0
#image= Image.open('dino.jpg')
#while i < total_per:
    #condition=permu_array[i]
    #fps=condition[0]
    #iso=condition[1]
    #i=i+1
    #print('Condition:',condition,' fps:',str(fps),' iso:',str(iso))
    #image.save('my_dino_FR%s_ISO%s.jpg' %(fps,iso))

#Image naming using foor loop
image= Image.open('dino1.jpg')
for i in range(total_per):
    condition=permu_array[i]
    fps=condition[0]
    iso=condition[1]
    i=i+1
    #print('Condition:',condition,' fps:',str(fps),' iso:',str(iso))
    image.save('my_dino_FR%s_ISO%s.jpg' %(fps,iso))
    
#c = str(input('. . . Press [Enter] to continue >'))
