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


class FFTnotInit(Exception):
   def __init__(self, value):
       self.value = value
   def __str__(self):
       return "Fourier transform not initialized"


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
            raise FFTnotInit("idek")
        return cc