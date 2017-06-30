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
        img = mpimg.imread(filepathname)
        img = MyRGBImg(img)
        
        
        if img.data.shape[2] == 4:
            colors = []
            for i in range(3):
                channel = img.get_channel(i)
                colors.append(channel)
            
            # initializate the image
            myimage = MyRGBImg(data = np.zeros((img.data.shape[0],
                                                img.data.shape[1],
                                                3)))
            for i in range(3):
                channel = colors[i]
                channel.data = np.transpose(channel.data)
                myimage.set_channel(channel, i)
            self.data = myimage.data
        else:
            self.data = img.data
        
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
        if type(channel) == str:
            c2idx ={'r':0, 'g':1, 'b':2}
        else:
            c2idx = [0, 1, 2]
        return MyImage(self.data[:,:,c2idx[channel]])
    
    def set_channel(self, image, channel):
        if type(channel) == str:
            c2idx ={'r':0, 'g':1, 'b':2}
        else:
            c2idx = [0, 1, 2]
        img = image.data
        #hack... don't know whyp
        datadimx = self.data.shape[0]
        datadimy = self.data.shape[1]
        imgdimx = img.shape[0]
        imgdimy = img.shape[1]
        if imgdimx != datadimx or imgdimy != datadimy:
            img = np.transpose(img)

        self.data[:,:,c2idx[channel]] = img
    
    def move(self, idx, idy):
        dx = idx
        dy = -idy
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
    
    def rotate(self, angle, center = (0,0)):
        # split channels
        angle = -angle
        for c in range(3):
            ch = self.get_channel(c)
            ch.rotate(angle, center)
            self.set_channel(ch, c)
    
    def squareit(self):
        lx = self.data.shape[0]
        ly = self.data.shape[1]
        
        dim = ly if lx > ly else lx
        
        newpic = MyRGBImg(data = np.zeros((dim, dim, 3)))

        for c in range(3):
            ch = self.get_channel(c)
            ch.squareit()
            newpic.set_channel(ch, c)
        
        self.data = newpic.data
    
    def transpose(self):
        for c in range(3):
            ch = self.get_channel(c)
            ch.transpose()
            self.set_channel(ch, c)
   
    
if __name__ == "__main__":
    # load a sample rgb picture

    path = "../../../silentcam/dataset25/1497791410073.jpg"
    path = "../../../silentcam/dataset25/avg/aligned_rgb_images/alg_1497791410073.png"
    path = "../../../Lenna.png"
    path = "../../../images.png"
    
    myimg = MyRGBImg()
    myimg.read_from_file(path)
    myimg.squareit()
    
    myimg.show_image()
    plt.show()
    
    
    myimg.inspect('r')
    
    mvimg = deepcopy(myimg)
    mvimg.move(100, 100)
    mvimg.show_image()
    plt.show()
    
    mvimg.inspect('r')
    
#    path = "../../../silentcam/dataset25/rgbtest/mov_1497791410073.png"
#    mvimg.save(path)

    # rotate image
    rotimg = deepcopy(myimg)
    rotimg.rotate(10, ( -88, 0))
    rotimg.show_image()
    plt.show()    
    