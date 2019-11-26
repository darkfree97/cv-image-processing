import cv2
import numpy as np
from matplotlib import pyplot as plt


def display(title1: str, image1, title2: str, image2):
    plt.subplot(121), plt.imshow(image1, cmap='gray')
    plt.title(title1), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(image2, cmap='gray')
    plt.title(title2), plt.xticks([]), plt.yticks([])
    plt.show()


img = cv2.imread('../cup.jpg', 0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))
dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

display('Input Image', img, 'Magnitude Spectrum', magnitude_spectrum)

# ----------------------------------------------------------------
rows, cols = img.shape
crow, ccol = rows//2, cols//2

# ----------------------------------------------------------------

# fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
# f_ishift = np.fft.ifftshift(fshift)
# img_back = np.fft.ifft2(f_ishift)
# img_back = np.abs(img_back)
#
#
# plt.subplot(131),plt.imshow(img, cmap = 'gray')
# plt.title('Input Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(132),plt.imshow(img_back, cmap = 'gray')
# plt.title('Image after HPF'), plt.xticks([]), plt.yticks([])
# plt.subplot(133),plt.imshow(img_back)
# plt.title('Result in JET'), plt.xticks([]), plt.yticks([])
#
# plt.show()

# ----------------------------------------------------------------

# create a mask first, center square is 1, remaining all zeros
mask = np.zeros((rows, cols, 2), np.uint8)
mask[crow-30:crow+30, ccol-30:ccol+30] = 1

# apply mask and inverse DFT
fshift = dft_shift*mask
f_ishift = np.fft.ifftshift(fshift)
img_back = cv2.idft(f_ishift)
img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

display('Input Image', img, 'Magnitude Spectrum', img_back)
