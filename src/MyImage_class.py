# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:33:12 2017

@author: Mauro
"""

# Image handling class

# Define Imports

# numpy, scipy, matlibplot imports
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy import signal

# py imports
from copy import deepcopy

class MyImage(object):
    
    # initialization functions
    
    def __init__(self, data = np.zeros((5,5))):
        
        if type(data) == np.ndarray:
            self.data = data
        elif isinstance(data, tuple):
            if len(data) == 2:
                self.data = np.zeros(data)
        else:
            raise ValueError("data type not supported")
            
    
    # debug options
    
    def inspect(self, output = True):
        # short function that returns a string with the image values
        
        m = np.mean(self.data)
        s = np.std(self.data)
        u = np.max(self.data)
        l = np.min(self.data)
        d = self.data.shape
        
        if output:
            s  = "Mean: {0:.2f} | Std: {1:.2f} | Max: {2:.2f}|Min: {3:.2f} | Dim: {4[0]}x{4[1]}".format(m, s, u, l, d)
            print(s)
            return s
            
        return (m, s, u, l, d)   
    
    def show_image(self):
        # show the picture data
        data = deepcopy(self.data)
        mi = np.min(data)
        pospic = data + mi
        m = np.max(pospic)
        npic = pospic / float(m)
        data = 1 - npic     
        plt.imshow(np.transpose(data), cmap = "Greys")    

    
    # I/O functions
    
    def read_from_file(self, filepathname):
        # import image from file
        # todo warnings about file existing
        self.data = mpimg.imread(filepathname)

    def save(self, filename):
        plt.imsave(filename, self.data)    


    # operators overload        
    def __add__(self, rhs):
        self.data = self.data + rhs.data
        return MyImage(self.data)
    
    def __truediv__(self, rhs):
        rpic = deepcopy(self.data)
        for x in range(self.data.shape[0]):
            for y in range(self.data.shape[1]):
                rpic[x][y] = self.data[x][y] / rhs
        
        return MyImage(rpic)


    # editing functions
    
    def create_composite_right(self, rhsimage):
        # enlarge the array to fit the next image
        self.data = np.concatenate((self.data, rhsimage.data), axis = 1)
    
    def normalize(self):
        #normalize the picture ( ( x- mean) / std ) 
        m = np.mean(self.data)
        s = np.std(self.data)
        self.data = (self.data - m) / s

    def convert2grayscale(self):
        self.data = np.dot(self.data[...,:3], [0.299, 0.587, 0.114])
    
    def transpose(self):
        self.data.transpose()
        
    def binning(self, n = 1):
        for i in range(n):
            rimg = np.zeros( (int(self.data.shape[0] / 2) , int(self.data.shape[1] / 2)))
        
            for x in range(rimg.shape[0]):
                for y in range(rimg.shape[1]):
                    a = self.data[x*2]    [y*2]
                    b = self.data[x*2 + 1][y*2]
                    c = self.data[x*2]    [y*2 + 1]
                    d = self.data[x*2 + 1][y*2 + 1]
                    rimg[x][y] =  (a + b + c + d) / 4.0
            self.data = rimg

    def move(self, dx, dy):
        dx = -dx
        mpic = np.zeros(self.data.shape)
        mpiclenx = mpic.shape[0]
        mpicleny = mpic.shape[1]
        
        for x in range(mpiclenx):
            for y in range(mpicleny):
                xdx = x + dx
                ydy = y + dy
                if xdx >= 0 and xdx < mpiclenx and ydy >= 0 and ydy < mpicleny:
                    mpic[x][y] = self.data[xdx][ydy]
        
        self.data = mpic
    
    def squareit(self):
        lx = self.data.shape[0]
        ly = self.data.shape[1]
        
        if lx > ly:
            self.data = self.data[0:ly,0:ly]
        else:
            self.data = self.data[0:lx,0:lx]
    
    def correlate(self, image):
        corr = signal.correlate2d(image.data, self.data, boundary='symm', mode='same')
        return Corr(corr)

    def limit(self, valmax):
        mi = np.min(self.data)
        pospic = self.data + mi
        m = np.max(pospic)
        npic = pospic / float(m)
        self.data = npic * valmax
    
    def apply_mask(self, mask):
        self.data = self.data * mask.data
        

class Corr(MyImage):
    
    def find_peak(self, msize = 5):
        #' consider a matrix of some pixels
        matrixsize = msize
        # get the values
        best = (0,0,0)
        for x in range(self.data.shape[0] - matrixsize):
            for y in range(self.data.shape[1] - matrixsize):
                s = 0
                for i in range(matrixsize):
                    for j in range(matrixsize):
                        s += self.data[x + i][y + j]
                s =  s / float(matrixsize)**2
        
                if s > best[0]:
                    best = (s, x, y)
        return best
    
    def find_translation(self, msize = 5):
        best = self.find_peak(msize)
        dx = -(self.data.shape[0]/2 - best[1])
        dy = self.data.shape[1]/2 - best[2]
        return int(dx), int(dy)
    
    def show_translation(self, dx, dy):
        odx = dx + self.data.shape[0]/2
        ody = self.data.shape[1]/2 - dy
        plt.scatter(odx, ody, s=40, alpha = .5)       


class Mask(MyImage):
    
    def create_circle_mask(self, radius, smooth):
        # create an array in np
        dims = self.data.shape
        mask = np.ones(dims)*0.5
        center = (dims[0]/2.0, dims[1]/2.0)
        for i in range(dims[0]):
            for j in range(dims[1]):
                dcenter = np.sqrt( (i - center[0])**2 + (j - center[1])**2)
                if dcenter > (radius + smooth):
                    mask[i][j] = 0
                elif dcenter < (radius - smooth):
                    mask[i][j] = 1
                else:
                    y = -1*(dcenter - (radius + smooth))/radius
                    mask[i][j] = y
        self.data = mask
        self.limit(1) 
        return self.data
    
    def invert(self):
        self.data = 1 - self.data 
    
    def bandpass(self, rin, sin, rout, sout):
        if rin != 0:
            self.create_circle_mask(rin, sin)
        else:
            self.data = np.zeros(self.data.shape)
        
        bigcircle = deepcopy(self)
        bigcircle.create_circle_mask(rout, sout)
        bigcircle.invert() 
      
        m = (self + bigcircle)
    
        m.limit(1)
        m.invert()  
        
        self.data = m.data
    
    def __add__(self, rhs):
        self.data = self.data + rhs.data
        return Mask(self.data)
    
    
if __name__ == "__main__":
    mypicname = "../../../griglia.png"
    mypic = MyImage()
    mypic.read_from_file(mypicname)
    mypic.squareit()
    mypic.convert2grayscale()
    mypic.normalize()
    
    mypic.show_image()
    plt.show()
    
    movpic = deepcopy(mypic)
    movpic.move(100, 0)
    
    movpic.show_image()
    plt.show()
    
    # test correlation
#    cc = mypic.correlate(movpic)
#    
#    cc.show_image()
#    
#    dx, dy = cc.find_translation()
#    cc.show_translation(dx, dy)
#    plt.show()
    
    mypic.create_composite_right(movpic)

    mypic.show_image()
    plt.show()
    
    