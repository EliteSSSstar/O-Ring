#Start

#Imports
import cv2 as cv
import numpy as np
import time

#read in an image into memory
img = cv.imread('C:/Users/adam9/OneDrive/Documents/GitHub/O-Ring/Orings/cameraman.png',0)
copy = img.copy()
#check out some of its pixel values...img[x,y]..try different x and y values
x = 100
y = 100
pix = img[x,y]
print("The pixel value at image location [" + str(x) + "," + str(y) + "] is:" + str(pix))

# Image Histogram 

# Create histogram array for 256 grayscale values
# counts brightness values in the image
hist = np.zeros(256)

for x in range(img.shape[0]):
    for y in range(img.shape[1]):
        hist[img[x,y]] += 1 

# Threshold automatic
# Choose the threshold based on histogram peak
thresh = np.argmax(hist)

print("Chosen threshold:", thresh)



#implement thresholding ourselves using loops (soooo slow in python)
before = time.time()
thresh = 100
for x in range(0, img.shape[0]):
    for y in range(0, img.shape[1]):
        if img[x,y] > thresh:
            img[x,y] = 255
        else:
            img[x,y] = 0
after = time.time()
print("Time taken to process hand coded thresholding: " + str(after-before))

cv.imshow('thresholded image 1',img)
cv.waitKey(0)

# Binary Morphology- Closes any interior Holes

clean = img.copy() # copy of the thresholded image so we dont overwrite the original

# Loop through the image but avoid the edges
for x in range(1, img.shape[0]-1):
    for y in range(1, img.shape[1]-1):
        
        # Takes a 3x3 region around the current pixel
        region = img[x-1:x+2, y-1:y+2]

        # If most pixels in the region are white keep them white, helps remove small black holes.
        if np.sum(region) > 255*4:
            clean[x,y] = 255

# Show Display
cv.imshow('cleaned image', clean)
cv.waitKey(0)

# Extract the Regions properties
# Counting White Pixels in area
area = np.sum(clean == 255)
print("Region area:", area)

# pass Or Fail
if area < 5000:
    result = "FAIL"
else:
    result = "PASS"

# Show Display/ Annotation
cv.putText(clean,
           result,
           (30,40),
           cv.FONT_HERSHEY_SIMPLEX,
           1,
           255,
           2)

cv.imshow('final result', clean)
cv.waitKey(0)


#now lets use the opencv built in function to threshold the image
before = time.time()
#ret,copy = cv.threshold(copy,100,255,cv.THRESH_BINARY)
after = time.time()
print("Time taken to process opencv built in thresholding: " + str(after-before))
cv.imshow('thresholded image 2',copy)
cv.waitKey(0)
cv.destroyAllWindows()

#End