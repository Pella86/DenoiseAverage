# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 20:11:22 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

from copy import deepcopy

import numpy as np
from numpy import fft

import Image

#==============================================================================
# FFT class
#==============================================================================

class FFT:
    
    def __init__(self, image):
        self.ft = self.calc_ft(image)

    def calc_ft(self, image):
        return fft.fftshift(fft.fft2(image.channels[0].pixels))
    
    def calc_ift(self):
        return np.real(fft.ifft2(fft.fftshift(self.ft)))

    def power_spectrum(self):
        absolutefft = np.abs(self.ft)
        xlen = absolutefft.shape[0]
        ylen = absolutefft.shape[1]
        squareftt = deepcopy(absolutefft)
        for i in range(xlen):
            for j in range(ylen):
                if squareftt[i][j] != 0:
                    squareftt[i][j] = np.log(squareftt[i][j])**2
        realpart = np.real(squareftt)
        ps = Image.Image(realpart)
        
        return ps
    
    def correlate(self, imgfft):
        '''Very much related to the convolution theorem, the cross-correlation
            theorem states that the Fourier transform of the cross-correlation of
            two functions is equal to the product of the individual Fourier
            transforms, where one of them has been complex conjugated:  '''
        
        imgcj = np.conjugate(self.ft)
        imgft = imgfft.ft
        
        prod = deepcopy(imgcj)
        for x in range(imgcj.shape[0]):
            for y in range(imgcj.shape[1]):
                prod[x][y] = imgcj[x][y] * imgft[x][y]
        
        cc = Image.Corr(np.real(fft.ifft2(fft.fftshift(prod)))) # real image of the correlation
        
        # adjust to center
        cc.channels[0].pixels = np.roll(cc.channels[0].pixels, int(cc.channels[0].pixels.shape[0] / 2), axis = 0)
        cc.channels[0].pixels = np.roll(cc.channels[0].pixels, int(cc.channels[0].pixels.shape[1] / 2), axis = 1)

        return cc