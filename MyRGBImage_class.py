# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:24:50 2017

@author: Mauro
"""

# RGB Image handling class

# Define Imports

# numpy, scipy, matlibplot imports
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# py imports
from copy import deepcopy

# my imports
from MyImage_class import MyImage

class MyRGBImg(object):
    
    # initialization methods
    def __init__(self, data = np.zeros((5,5,3)), normalize = True):
        self.data = data
        if normalize:
            self.limit(1)
    
    # I/O methods
    def read_from_file(self, filepathname, normalize = True):
        # import image from file
        # todo warnings about file existing
        self.data = mpimg.imread(filepathname)
        if normalize:
            self.limit(1)

    
    def save(self, filename):
        plt.imsave(filename, self.data)
    
    # debug functions
    def inspect(self, channel):
        self.get_channel(channel).inspect(True)
     
    def show_image(self):
        plt.imshow(self.data)
        
    # edit picture
    def limit(self, valmax):
        mi = np.min(self.data)
        pospic = self.data + mi
        m = np.max(pospic)
        if m != 0:
            npic = pospic * (1 / float(m))
            self.data = npic * valmax

    def get_channel(self, channel):
        c2idx ={'r':0, 'g':1, 'b':2}
        return MyImage(self.data[:,:,c2idx[channel]])
    
    def set_channel(self, image, channel):
        c2idx ={'r':0, 'g':1, 'b':2}
        img = 255 - image.data
        self.data[:,:,c2idx[channel]] = img.transpose()
    
    def move(self, idx, idy):
        dx = idy
        dy = -idx
        mpic = np.zeros(self.data.shape)
        mpiclenx = mpic.shape[0]
        mpicleny = mpic.shape[1]
        
        for x in range(mpiclenx):
            for y in range(mpicleny):
                xdx = x + dx
                ydy = y + dy
                if xdx >= 0 and xdx < mpiclenx and ydy >= 0 and ydy < mpicleny:
                    for c in range(3):
                        mpic[x][y][c] = self.data[xdx][ydy][c]
                        if mpic[x][y][c] <= 0:
                            mpic[x][y][c] = 0
                        if mpic[x][y][c] >= 1:
                            mpic[x][y][c] = 1
        self.data = mpic
    
    # operator overload    
    def __add__(self, rhs):
        self.data = self.data + rhs.data
        return MyRGBImg(self.data)
    
    def __truediv__(self, rhs):
        rpic = deepcopy(self.data)
        for x in range(self.data.shape[0]):
            for y in range(self.data.shape[1]):
                for c in range(3):
                    rpic[x][y][c] = self.data[x][y][c] / rhs
        
        return MyRGBImg(rpic)
    
        
    
if __name__ == "__main__":
    # load a sample rgb picture

    path = "../../silentcam/dataset25/1497791410073.jpg"
    
    myimg = MyRGBImg()
    myimg.read_from_file(path)
    
    myimg.show_image()
    plt.show()
    
    myimg.inspect('r')
    
    mvimg = deepcopy(myimg)
    mvimg.move(100, 100)
    mvimg.show_image()
    plt.show()
    
    mvimg.inspect('r')
    
    path = "../../silentcam/dataset25/rgbtest/mov_1497791410073.png"
    mvimg.save(path)
    
    
    