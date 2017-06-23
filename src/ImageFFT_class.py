# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 19:26:28 2017

@author: Mauro
"""

# Image handling class

# Define Imports

# numpy, scipy, matlibplot imports
import numpy as np
from numpy import fft

# py imports
from copy import deepcopy

# my imports
from MyImage_class import MyImage, Corr


#==============================================================================
# # Exceptions
#==============================================================================
class FFTnotInit(Exception):
   def __init__(self, value = 0):
       self.value = value
   def __str__(self):
       return "FFTerror: Fourier transform not initialized"

class FFTimagesize(Exception):
   def __init__(self, value):
       self.value = value
   def __str__(self):

      return "FFTerror: Image size not supported {0} | {1}".foramt(self.value[0], self.value[1])


#       try:
#           return "FFTerror: Image size not supported {0} | {1}".foramt(self.value[0], self.value[1])
#       except:
#           return "wtf dude??"

#==============================================================================
# # classes
#==============================================================================

class myFFT(object):
    def __init__(self, ft):
        self.ft = ft
    
    def ift(self):
      return MyImage(np.real(fft.ifft2(fft.fftshift(self.ft))))

class ImgFFT(object):
    
    
    # initialize functions
    #  the class has two behaviors one is the standard and lets the user decide
    #  when to apply specific functions
    #  the other is when a mask is given and the function will automatically 
    #  calculate the images
    def __init__(self, myimage, mask = False):
        self.img = myimage         # original image
        self.imgfft = 0            # fourier transform
        self.imgifft = MyImage()   # inverted fourier transform 
        self.ps = 0                # power spectrum
        
        if mask:
            self.ft()
            self.power_spectrum()
            self.apply_mask(mask)
            self.ift()
    
    def auto(self):
        # this function automatize the initializazion and calculates ps and 
        # fft
        self.ft()
        self.power_spectrum()
            
    
    # image editing functions
    def ft(self):
        self.imgfft = fft.fftshift(fft.fft2(self.img.data))
    
    def ift(self):
        self.imgifft = MyImage(np.real(fft.ifft2(fft.fftshift(self.imgfft))))
        
    def power_spectrum(self):
        absolutefft = np.abs(self.imgfft)
        xlen = absolutefft.shape[0]
        ylen = absolutefft.shape[1]
        squareftt = deepcopy(absolutefft)
        for i in range(xlen):
            for j in range(ylen):
                if squareftt[i][j] != 0:
                    squareftt[i][j] = np.log(squareftt[i][j])**2
        realpart = np.real(squareftt)
        ps = MyImage(realpart)
        
        self.ps = ps
    
    def apply_mask(self, mask):
        self.imgfft = self.imgfft * mask.data
    
    # Correlate functions
    
    def correlate(self, imgfft):
        #Very much related to the convolution theorem, the cross-correlation
        #theorem states that the Fourier transform of the cross-correlation of
        #two functions is equal to the product of the individual Fourier
        #transforms, where one of them has been complex conjugated:  
        
        
        if self.imgfft is not 0 or imgfft.imgfft is not 0:
            imgcj = np.conjugate(self.imgfft)
            imgft = imgfft.imgfft
            
            prod = deepcopy(imgcj)
            for x in range(imgcj.shape[0]):
                for y in range(imgcj.shape[0]):
                    prod[x][y] = imgcj[x][y] * imgft[x][y]
            
            cc = Corr( np.real(fft.ifft2(fft.fftshift(prod)))) # real image of the correlation
            
            # adjust to center
            cc.data = np.roll(cc.data, int(cc.data.shape[0] / 2), axis = 0)
            cc.data = np.roll(cc.data, int(cc.data.shape[1] / 2), axis = 1)
        else:
            raise FFTnotInit()
        return cc
    
    def resize_image(self, sizex, sizey):
        imsizex = self.img.data.shape[0]
        imsizey = self.img.data.shape[1]
        
        if sizex > imsizex or sizey > imsizey:
            raise FFTimagesize((sizex, sizey))
        else:
            l2x = imsizex / 2
            l2y = imsizex / 2
            
            if self.imgfft is 0:
                raise FFTnotInit()
            else:
                xl = int(l2x - sizex / 2)
                xu = int(l2x + sizex / 2)
                yl = int(l2y - sizey / 2)
                yu = int(l2y + sizey / 2)
                fftresized = myFFT(self.imgfft[xl : xu, yl : yu])
                return fftresized.ift()
                
                
if __name__ == "__main__":
    
    from matplotlib import pyplot as plt
    
    # load sample image
    imagepath = "C:/Users/Mauro/Desktop/Vita Online/Programming/Picture cross corr/Lenna.png"
    imagepath = "C:/Users/Mauro/Desktop/Vita Online/Programming/Picture cross corr/silentcam/dataset24/avg/correlation_images/corr_1497777846958.png"

    
    im = MyImage()
    im.read_from_file(imagepath)
    im.convert2grayscale()

    im.show_image()
    plt.show()
   
    ft = ImgFFT(im)
    ft.ft()
    
    re = ft.resize_image(100, 100)
    
    
    
    re.show_image()
    plt.show()
    