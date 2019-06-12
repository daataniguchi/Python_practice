#variables:
#fps_top is the max(top) frame rate limit
#fps_bottom is the min(bottom) frame rate limit
#fps_increment is the increment value
#fps_lst the list in which frame rates will go, starting with the lower limit
fps_top=30
fps_bottom=15
fps_increment=10
fps_lst=[fps_bottom]

#While loop:
while fps_bottom < fps_top:                             #Conditions set for the while loop: while top limit < bottom limit
    fps_bottom=fps_bottom+fps_increment                 # addition of fps_increment + fps_bottom= fps_bottom
    fps_lst.append(fps_bottom)                          # appending the new fps_bottom value to fps_lst
    
#if loop was added to avoid any number greater than top limit from being included in the list
#regardless of the increments
if fps_lst[len(fps_lst)-1] > fps_top:                   #If the last number is greater than the top limit
    fps_lst.pop()                                       #Then it will be popped out (won't be included
                                                        #in final list)
    
print(fps_lst)

#variables:
#iso_top is the max(top) iso limit
#iso_bottom is the min(bottom) iso limit
#iso_increment is the increment value
#iso_lst the list in which ISO values will go, starting with the lower limit
iso_top=800
iso_bottom=100
iso_increment=150

iso_lst=[iso_bottom]

#While loop to cycle though increment values
while iso_bottom < iso_top:                             # Conditions for the while loop: while the iso bottom limit is < iso top limit
    iso_bottom=iso_bottom+iso_increment                 # add iso_bottom and increments to replace iso_bottom valeu (Adding itself + increment)
    iso_lst.append(iso_bottom)                          # append the new iso_bottom value to iso_lst
    
# If loop added to avoid any number greater than top limit from being included in the list regardless of increments
if iso_lst[len(iso_lst)-1] > iso_top:                   # if the last number is greater than top limit it will be popped out
    iso_lst.pop()                                       # and it won't be included in final list
    
print(iso_lst)
