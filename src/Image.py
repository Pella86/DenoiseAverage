# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 09:08:15 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

import Channel


#==============================================================================
# image class
#==============================================================================

class Image:
    
    def __init__(self, indata):
        
        self.channels = []
        self.filename = ""
        
        if type(indata) is str:
            self.load_image(indata)
            self.filename = indata
        elif type(indata) is tuple:

            dimx = indata[0]
            dimy = indata[1]
            if len(indata) == 3:
                nch = indata[2]
            else:
                nch = 1
            
            for i in range(nch):
                ch = Channel.Channel(np.zeros((dimx, dimy)))
                self.channels.append(ch)
        else:
            self.channels.append(Channel.Channel(indata))
    
    # ----- getters setters -----
    
    def get_size(self):
        return self.channels[0].get_size()
    
    # ----- I/O functions -----
    def load_image(self, filename):
        ''' Read the image from file '''
        
        # clear channels
        self.channels = []
        
        # read the image
        data = mpimg.imread(filename)
        
        # append channels to the image channels
        if len(data.shape) == 2:
            ch = Channel.Channel(data)
            self.channels.append(ch)
        elif len(data.shape) == 3 or len(data.shape) == 4:
            for ich in range(3):
                ch = Channel.Channel(data[:, :, ich])
                self.channels.append(ch)
    
    
    def convert_rgb_image_to_nparray(self):
        ''' This function conversts the 3 channel layer in a np array used for
        save and display'''
        if len(self.channels) != 3:
            raise "conversion is needed only for rgb images"
        
        dimx, dimy = self.channels[0].get_size()
       
        data = np.zeros((dimx, dimy, 3))
        for ich in range(3):
            data[:, :, ich] = self.channels[ich].pixels
        
        return data
    
    def save_image(self, filename):
        ''' save image on disk '''
        if len(self.channels) == 1:
            data = self.channels[0].pixels
        elif len(self.channels) == 3:
            data = self.convert_rgb_image_to_nparray()
        
        mpimg.imsave(filename, data, cmap="Greys_r") 
    
    def display(self):
        ''' display the image with pyplot using imshow'''
        if len(self.channels) == 1:
            self.channels[0].display()
        elif len(self.channels) == 3:
            data = self.convert_rgb_image_to_nparray()
            
            plt.imshow(data)
            
    # ----- Operators functions -----
    
    def __add__(self, rhs):
        if len(self.channels) != len(rhs.channels): raise Exception("the images have to have equal number of channels")
        for i, ch in enumerate(self.channels):
            ch += rhs.channels[i]
        return self
    
    # ----- Editing functions -----
    
    def normalize(self):
        if len(self.channels) != 1:
            raise Exception("RGB Mode not supported for normalization")
            
        for ch in self.channels:
            ch.normalize()
    
    def transpose(self):
        for ch in self.channels:
            ch.transpose()
    
    def binning(self, n):
        for ch in self.channels:
            ch.binning(n)
    
    def move(self, dx, dy):
        for ch in self.channels:
            ch.move(dx, dy)
    
    def crop(self, x, y, dimx, dimy = None):
        for ch in self.channels:
            ch.crop(x, y, dimx, dimy)
    
    def convert_to_bw(self):
        if len(self.channels) != 3: raise Exception("can't convert other than rgb images")
        
        dimx, dimy = self.get_size()
        
        rchannel = Channel.Channel(np.zeros((dimx, dimy)))
        
        for x in range(dimx):
            for y in range(dimy):
                factors = [0.299, 0.587, 0.114]
                v = 0
                for c in range(3):
                    v += self.channels[c].pixels[x, y] * factors[c]
        
                rchannel.pixels[x, y] = v

        self.channels = []
        self.channels.append(rchannel)
    
    def limit(self, valmax):
        for ch in self.channels:
            ch.limit(valmax)
    
    def restrict(self, sigma):
        for ch in self.channels:
            ch.restrict(sigma)
    
    def rotate(self, deg, center = (0, 0)):
        for ch in self.channels:
            ch.rotate(deg, center)

class Corr(Image):
    
    def __init__(self, pixels):
        self.channels = []
        self.channels.append(Channel.Corr_ch(pixels))
    
    def find_peak(self, msize = 5):
        return self.channels[0].find_peak(msize)
        
    def find_translation(self, peak = None):
        return self.channels[0].find_translation(peak)    

    def show_translation(self, dx, dy):
        return self.channels[0].show_translation(dx, dy)    
                
                
            
        