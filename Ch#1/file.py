import numpy as np
# import scipy
import cv2

image = cv2.imread('test.jpg')
cv2.imwrite('new_image.png',image)