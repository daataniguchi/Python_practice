import time                                                            
import RPi.GPIO as GPIO
from picamera import PiCamera                                         
import os
from subprocess import check_output
from datetime import datetime
import numpy as np
from PIL import Image

GPIO.setwarnings(False)

i = 0
light = 12
wifi = 7

ping_hub = "ping 192.168.0.1 -c 1"

subp = "sudo pkill -9 -f ADXL345_Sampler_100Hz.py"


#Looping through frame rate:

fps_top=30                                              #fps_top is the max(top) frame rate limit
fps_bottom=15                                           #fps_bottom is the min(bottom) frame rate limit
fps_increment=12                                        #fps_increment is the increment value
fps_lst=[fps_bottom]                                    #fps_lst the list in which frame rates will go, starting with the lower limit



while fps_bottom < fps_top:                             #Conditions set for the while loop: while top limit < bottom limit
    fps_bottom=fps_bottom+fps_increment                 # addition of fps_increment + fps_bottom= fps_bottom
    fps_lst.append(fps_bottom)                          # appending the new fps_bottom value to fps_lst
    
if fps_lst[len(fps_lst)-1] > fps_top:                   #If the last number is greater than the top limit
    fps_lst.pop()                                       #Then it will be popped out (won't be included in final list)

#Looping though ISO:

iso_top=800                                             #iso_top is the max(top) iso limit
iso_bottom=100                                          #iso_bottom is the min(bottom) iso limit
iso_increment=250                                       #iso_increment is the increment value
iso_lst=[iso_bottom]                                    #iso_lst the list in which ISO values will go, starting with the lower limit


while iso_bottom < iso_top:                             # Conditions for the while loop: while the iso bottom limit is < iso top limit
    iso_bottom=iso_bottom+iso_increment                 # add iso_bottom and increments to replace iso_bottom valeu (Adding itself + increment)
    iso_lst.append(iso_bottom)                          # append the new iso_bottom value to iso_lst
    

if iso_lst[len(iso_lst)-1] > iso_top:                   # if the last number is greater than top limit it will be popped out and it won't be included in final list
    iso_lst.pop()                                   

#Combinding both lists to get all possible permutations
#Total permutations saved on total_per
combo=[]
total_per=0

for a in fps_lst:              #for a variable (a) in list 1
    for b in iso_lst:          #for a variable (b) in list 2
        combo.append([a,b])    #append variables a and b into list called combo
        total_per=total_per+1
        
        
#Making an array called permu_array and placing it in a list       
permu_array=np.array(combo)
permu_array=combo

#Image naming using for loop
image= Image.open('dino1.jpg')
for i in range(total_per):
    condition=permu_array[i]
    fps=condition[0]
    iso=condition[1]
    
    #print('Condition:',condition,' fps:',str(fps),' iso:',str(iso))
    #image.save('my_dino_FR%s_ISO%s.jpg' %(fps,iso))

#Camera Functions:

def off():                                                                                  #Camera off
    GPIO.output(light, 0)
    
def on():                                                                                   #Camera on
    GPIO.output(light, 1)

def picture(fr,iso):
    camera.resolution = (2592, 1944)                                                        #Camera resolution
    camera.framerate = fr                                                                   #fr assigned to camera.framerate in picture function
    camera.iso= iso                                                                         #iso assigned to camera.iso in picture function
    camera.start_preview()
    pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4]                          #pictime assigned to time photo was taken displaying in Years_month_day_hour-minute-seconds
    time.sleep(10)
    camera.capture('/home/pi/Documents/minion_pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso))    #Directory where photo is saved and naming format
    camera.stop_preview()

def send():
    who = check_output("who",shell=True)
    who = who.split('(')[1]
    ip = who.split(')')[0]
#   print(ip)
    scp = "sudo sshpass -p 'ramboat' scp /home/pi/Documents/minion_pics/%s.jpg jack@%s:/home/jack/minion_pics/" % (pictime, ip)
    os.system(scp) 
#   print(scp)


if __name__ == '__main__':

        status = os.system(ping_hub)

        if status == 0:
                status = "Connected"
                os.system(subp)
                quit()
        else:
                status = "Not Connected"


camera = PiCamera()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(wifi, GPIO.OUT)
GPIO.output(wifi, 1)

#   on()
for i in fps_lst:                    #loop through i in fps_lst and j in iso_lst and call the function picture.
    for j in iso_lst:		     #This will result in camera.framerate and camera.iso cycling through a different value, taking a photo and going to the next value.  
	picture(i,j)
        
#   off()
time.sleep(5)

#   status = os.system(ping_hub)
#
#   if status == 0:
#       status = "Connected"
#   else:
#       status = "Not Connected"
#
#   print(status)


if status == "Connected":
#       send()
        os.system(subp)
#       GPIO.output(wifi, 1)
#       quit()
else:
        GPIO.output(wifi, 0)
        time.sleep(6)
        os.system('sudo shutdown now')

