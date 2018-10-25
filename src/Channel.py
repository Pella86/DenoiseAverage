# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 09:06:24 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image


#==============================================================================
# helpers
#==============================================================================



def limit(data, valmax):
    ''' remaps the values from 0 to valmax'''
    mi = data.min()
    mi = np.abs(mi)
    pospic = data + mi
    m = np.max(pospic)
    npic = pospic / float(m)
    return npic * valmax    

#==============================================================================
# Channel class
#==============================================================================

class Channel:
    
    def __init__(self, px_matrix = np.zeros((512, 512))):
        self.pixels = px_matrix
    
    def __add__(self, rhs):
        self.pixels += rhs.pixels
        return self
    
    def display(self):
        pxdisp = limit(self.pixels, 1)
        plt.imshow(pxdisp, cmap="Greys_r")
    
    def get_size(self):
        return self.pixels.shape
    
    def normalize(self):
        ''' normalize channel with mean 0 and std 1'''
        m = np.mean(self.pixels)
        s = np.std(self.pixels)
        self.pixels = (self.pixels - m) / s
    
    def transpose(self):
        ''' transposes the picture '''
        self.pixels = self.pixels.transpose()
    
    def binning(self, n):
        ''' Averages a matrix of 2x2 pixels to one value, effectively reducing
        size by two and averaging the value, giving less noise. n indicates
        how many time the procedure is done 
        512x512 bin 1 -> 256x256 bin 2 -> 128128 bin 3 -> ...
        '''
        for i in range(n):
            # initialize resulting image
            dimx, dimy = self.get_size()
            rchannel = np.zeros( (int(dimx / 2) , int(dimy / 2)))
            rdimx, rdimy = rchannel.shape
            
            # calculate for each pixel the corresponding
            # idx rimg = 2*idx srcimg
            for x in range(rdimx):
                for y in range(rdimy):
                    values = []
                    for i in range(2):
                        for j in range(2):
                            v = self.pixels[x * 2 + i][y * 2 + j]
                            values.append(v)
                    
                    rchannel[x,y] =  np.mean(values)

            self.pixels = rchannel
    
    def move(self, idx, idy):
        ''' moves the picture by the dx or dy values. dx dy must be ints'''
        # correction to give dx a right movement if positive
        dx, dy = -idy, -idx
        
        # initialize the image
        rimg = np.zeros(self.pixels.shape)
        
        # get image size
        dimx, dimy = self.get_size()

        for x in range(dimx):
            for y in range(dimy):
                xdx = x + dx
                ydy = y + dy
                if xdx >= 0 and xdx < dimx and ydy >= 0 and ydy < dimy:
                    rimg[x][y] = self.pixels[xdx][ydy]
        
        self.pixels = rimg
    
    def crop(self, ix, iy, idimx, idimy = None):
        ''' crops the image given a starting point and the dimensions'''
        
        # if the y dim is none then make it a square
        if idimy is None:
            idimy = idimx

        # check sizes
        if ix < 0 or iy < 0: raise Exception("crop: Origin must be above 0")
        sizey, sizex = self.get_size()
        if ix + idimx > sizex: raise Exception("crop: Can't crop outside x borders, image dim {}, crop size {}".format(sizex, ix + idimx))
        if iy + idimy > sizey: raise Exception("crop: Can't crop outside y borders, image dim {}, crop size {}".format(sizey, iy + idimy))

        # invert the coords
        x, y = iy, ix
        dimx, dimy = idimy, idimx

        # crop the image
        rimg = self.pixels[x : x + dimx, y : y + dimy]
        self.pixels = rimg
        
    
    def limit(self, valmax):
        rimg = limit(self.pixels, valmax)
        self.pixels = rimg
        
    def restrict(self, sigma):
        # automatically limit the values to the 3 sigma from the distribution
        s = np.std(self.pixels)
        print(self.get_size())
        dimx, dimy = self.get_size()
        for x in range(dimx):
            for y in range(dimy):
                if self.pixels[x][y] > s * sigma:
                    self.pixels[x][y] = s * sigma
                
                if self.pixels[x][y] < -(s * sigma):
                    self.pixels[x][y] = -(s * sigma)
    
    def rotate(self, deg, center = (0, 0)):
        ''' rotates the image by set degree'''
        #where c is the cosine of the angle, s is the sine of the angle and
        #x0, y0 are used to correctly translate the rotated image.
#        self.normalize()
#        self.limit(255)
#        
#        image = Image.fromarray(self.pixels.astype("uint8"), 'L')
#        
#        rot = image.rotate(-deg)
#        
#        # convert in numpy array
#        self.pixels = np.array(rot.getdata(), np.uint8).reshape(rot.size[1], rot.size[0])

        
        # size of source image
        src_dimsx, src_dimsy = self.get_size()
        
        # get the radians and calculate sin and cos
        rad = np.deg2rad(-deg)
        c = np.cos(rad)
        s = np.sin(rad)
        
        # calculate center of image
        cx = center[0] + src_dimsx/2
        cy = center[1] + src_dimsy/2
        
        # factor that moves the index to the center
        x0 = cx - c*cx - s*cx
        y0 = cy - c*cy + s*cy
        
        # initialize destination image
        dest = np.zeros(self.get_size())
        for y in range(src_dimsy):
            for x in range(src_dimsx):
                # get the source indexes
                src_x = int(c*x + s*y + x0)
                src_y = int(-s*x + c*y + y0)
                if src_y > 0 and src_y < src_dimsy and src_x > 0 and src_x < src_dimsx:
                    #paste the value in the destination image
                    dest[x][y] = self.pixels[src_x][src_y]
                    
        self.pixels = dest

    
    def display_histogram(self):
        linear_pixels = self.pixels.flatten()
        plt.hist(linear_pixels, 100)

        

class Corr_ch(Channel):
    ''' This class provide additional methods in case the picture is a
    correlation picture.
    '''
    
    def find_peak(self, msize = 5):
        ''' finde the pixel with highest value in the image considers a matrix
        of msize x msize, for now works very good even if size is 1.
        returns in a tuple s, x, y. s is the corrrelation coefficient and
        x y are the pixel coordinate of the peak.
        '''
        #' consider a matrix of some pixels
        best = (0,0,0)
        for x in range(self.pixels.shape[0] - msize):
            for y in range(self.pixels.shape[1] - msize):
                # calculate mean of the matrix
                s = 0
                for i in range(msize):
                    for j in range(msize):
                        s += self.pixels[x + i][y + j]
                s =  s / float(msize)**2
                
                # assign the best value to best, the return tuple
                if s > best[0]:
                    best = (s, x, y)
        return best
    
    def find_translation(self, peak = None):
        ''' converts the peak into the translation needed to overlap completely
        the pictures
        '''
        if peak is None:
            peak = self.find_peak()
        
        #best = self.find_peak(msize)
        peakx = peak[2]
        peaky = peak[1]
        
        dx = self.pixels.shape[0]/2 - peakx
        dy = self.pixels.shape[1]/2 - peaky
        
        return int(dx), int(dy)
    
    def show_translation(self, dx, dy):
        ''' prints on the image where the peak is
        usage:
            corr = Corr()
            best = corr.find_peak()
            dx, dy = corr.find_translation(best)
            corr.show_image()
            corr.show_translation(dx, dy)
            plt.show()
        '''
        ody = dx + self.pixels.shape[0]/2
        odx = self.pixels.shape[1]/2 - dy
        plt.scatter(odx, ody, s=40, alpha = .5)
        return odx, ody
    


if __name__ == "__main__":
    
    import matplotlib.image as mpimg
    #test_image = "../data/Lena_BW.png"
    #test_image = r"C:\Users\Mauro\Desktop\Vita Online\Programming\Picture cross corr\samsung_S8\dataset_1\avg\avg.png"
    test_image = r"C:\Users\Mauro\Desktop\Vita Online\Programming\Picture cross corr\samsung_S8\test_dataset\preprocessed\pic_0.png"
    img = mpimg.imread(test_image)
    pxch = img[:, :, 0]
    ch = Channel(pxch)
    ch.display()
    plt.show()

    ch.normalize()
    ch.display_histogram()
    plt.show()
    
    ch.rotate(20)
    ch.display()
    plt.show()
