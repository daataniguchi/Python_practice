import cv2
import numpy
import glob
import pylab as plt

folders = glob.glob('/Users/keomonydiep/Desktop/training_images/ciliates')
for i in folders:
    image_list = []
    for f in glob.glob(i+'/*.jpg'):
        image_list.append(f)

read_images = []

for image in image_list:
    read_images.append(cv2.imread(image, cv2.IMREAD_GRAYSCALE))

#print(read_images[0:])

print(read_images)
plt.imshow(read_images[0])

