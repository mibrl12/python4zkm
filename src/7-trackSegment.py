"""
Clean and segment the autonomous trap image
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio
from scipy import ndimage
from skimage import color
from skimage import filters
from skimage import measure

imFile = "../data/t1.jpg"
im = imageio.imread(imFile)
print("Original shape: ",im.shape,", dtype: ",im.dtype)
im2 = color.rgb2gray(im)
print("Gray shape: ",im2.shape,", dtype: ",im2.dtype)

#optionally, add median before gauss
im3 = ndimage.median_filter(im2,3)
im3 = ndimage.gaussian_filter(im3, sigma=1.8)

#filters.try_all_threshold(im3)

im4 = im3 > filters.threshold_yen(im3)

# Remove small white regions
open_img = ndimage.binary_opening(im4,structure=np.ones((3,3))).astype(np.int)
# Remove small black hole
close_img = ndimage.binary_closing(open_img,structure=np.ones((3,3))).astype(np.int)

c = measure.find_contours(close_img,.5)
print("Number of contours: ",len(c))

f = plt.subplot(231)
plt.imshow(im)
f.set_title("Original\n")
plt.axis('off')
f = plt.subplot(232)
plt.imshow(im2, cmap=plt.cm.gray, interpolation='nearest')
f.set_title("Gray\n")
plt.axis('off')
f = plt.subplot(233)
plt.imshow(im3, cmap=plt.cm.gray, interpolation='nearest')
f.set_title("Gauss\n(+ Median)")
plt.axis('off')
f = plt.subplot(234)
plt.imshow(im4, cmap=plt.cm.gray, interpolation='nearest')
f.set_title("Threshold\n")
plt.axis('off')
f = plt.subplot(235)
plt.imshow(close_img, cmap=plt.cm.gray, interpolation='nearest')
f.set_title("Cleaned\n")
plt.axis('off')
f = plt.subplot(236)
plt.imshow(close_img, cmap=plt.cm.gray, interpolation='nearest')
plt.contour(close_img, [0.5], linewidths=2, colors='r')
f.set_title("Cleaned\n" + str(len(c)) + " contours")
plt.axis('off')


plt.subplots_adjust(wspace=0.02, hspace=0.3, top=.9, bottom=0.1, left=0, right=1)
plt.show()
