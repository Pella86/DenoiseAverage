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
from MyImage_class import MyImage, Corr, Mask


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
       s = "."
       try:
           s = "FFTerror: Image size not supported: {0} | {1}".format(self.value[0], self.value[1])
       except Exception as e:
           print(e)
           print(type(e))
          
       return s


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


def map_range(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class ImgFFT(object):
    
    
    # initialize functions
    #  the class has two behaviors one is the standard and lets the user decide
    #  when to apply specific functions
    #  the other is when a mask is given and the function will automatically 
    #  calculate the images
    def __init__(self, myimage, mask = False):
        self.img = myimage         # original image
        self.imgfft = None            # fourier transform
        self.imgifft = None   # inverted fourier transform 

        
        if mask:
            self.ft()
            self.power_spectrum()
            self.apply_mask(mask)
            self.ift()            
    
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
        
        return ps
    
    def apply_mask(self, mask):
        self.imgfft = self.imgfft * mask.data
    
    def get_real_part(self):
        r = MyImage(np.real(self.imgfft))       
        r.limit(1)        
        return r

    def get_imag_part(self):
        r = MyImage(np.imag(self.imgfft))  
        r.limit(1)
        return r
    # Correlate functions
    
    def get_magnitude(self):
        sizeimg = np.real(self.imgfft).shape
        mag = np.zeros(sizeimg)
        for x in range(sizeimg[0]):
            for y in range(sizeimg[1]):
                mag[x][y] = np.sqrt(np.real(self.imgfft[x][y])**2 + np.imag(self.imgfft[x][y])**2)
        rpic = MyImage(mag)
        rpic.limit(1)
        return rpic
    
    def get_phases(self):
        sizeimg = np.real(self.imgfft).shape
        mag = np.zeros(sizeimg)
        for x in range(sizeimg[0]):
            for y in range(sizeimg[1]):
                mag[x][y] = np.arctan2(np.real(self.imgfft[x][y]), np.imag(self.imgfft[x][y]))
        rpic = MyImage(mag)
        rpic.limit(1)
        return rpic    


#      int my = y-output.height/2;
#      int mx = x-output.width/2;
#      float angle = atan2(my, mx) - HALF_PI ;
#      float radius = sqrt(mx*mx+my*my) / factor;
#      float ix = map(angle,-PI,PI,input.width,0);
#      float iy = map(radius,0,height,0,input.height);
#      int inputIndex = int(ix) + int(iy) * input.width;
#      int outputIndex = x + y * output.width;
#      if (inputIndex <= input.pixels.length-1) {
#        output.pixels[outputIndex] = input.pixels[inputIndex];

    
    def get_polar_t(self):
        mag = self.get_magnitude()
        sizeimg = np.real(self.imgfft).shape
        
        pol = np.zeros(sizeimg)
        for x in range(sizeimg[0]):
            for y in range(sizeimg[1]):
                my = y - sizeimg[1] / 2
                mx = x - sizeimg[0] / 2
                if mx != 0:
                    phi = np.arctan(my / float(mx))
                else:
                    phi = 0
                r   = np.sqrt(mx**2 + my **2)
                
                ix = map_range(phi, -np.pi, np.pi, sizeimg[0], 0)
                iy = map_range(r, 0, sizeimg[0], 0, sizeimg[1])

                if ix >= 0 and ix < sizeimg[0] and iy >= 0 and iy < sizeimg[1]:
                    pol[x][y] =  mag.data[int(ix)][int(iy)]    
        pol = MyImage(pol)
        pol.limit(1)
        return pol
    
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
            raise FFTimagesize((imsizex, imsizey))
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
                imgfft = np.array(self.imgfft[xl : xu, yl : yu])
                fftresized = myFFT(imgfft)
                
                return fftresized.ift()
                
                
if __name__ == "__main__":
    
    from matplotlib import pyplot as plt
    
    # load sample image
    imagepath = "C:/Users/Mauro/Desktop/Vita Online/Programming/Picture cross corr/Lenna.png"
    imagepath = "C:/Users/Mauro/Desktop/Vita Online/Programming/Picture cross corr/silentcam/dataset24/avg/correlation_images/corr_1497777846958.png"
    
    imagepath = "../../../Lenna.png"
  
#    # convert range test
#    x = np.arange(0, 3, 0.1)
#    print(x)
#    
#    for i in x:
#        print(i, map_range(i, 0, 1, 0, 2*np.pi))
    
    im = MyImage()
    im.read_from_file(imagepath)
    im.convert2grayscale()
    
    print("Original image")
    im.show_image()
    plt.show()

   
    ft = ImgFFT(im)
    ft.ft()
    
    imres = ft.resize_image(256, 256)
    imres.show_image()
    plt.show()
    

#    print("Power Spectrum")    
#    ps = ft.power_spectrum()    
#    ps.show_image()
#    plt.show()
#    
#    real = ft.get_real_part()
#
#    print("Real image")
#    real.show_image()
#    plt.show()
#
#    print("Imaginary image")    
#    imag = ft.get_imag_part()
#    imag.show_image()
#    plt.show()    
#
#    print("Magnitude picture")    
#    magpic = ft.get_magnitude()
#    magpic.show_image()
#    plt.show()
#
#    print("Phase pic")    
#    p = ft.get_phases()
#    p.show_image()
#    plt.show()
#


#    testfolder= "../../../fftfun/PolarFFT/"
#    
#    print("Polar t pic")    
#    p = ft.get_polar_t()
#    p.show_image()
#    plt.show()
#
#    imft = ImgFFT(p)
#    imft.ft() 
#    
#    tsx = []
#    tsy = []
#    arange = np.arange(0, 90 + 10, 10)
#    for i in arange:
#        print("---------Angle: ", i,"----------")
#
#        myrot = deepcopy(im)    
#        myrot.rotate(i)    
#        myrot.show_image()
#        plt.show()
#    
#        ftrot = ImgFFT(myrot)
#        ftrot.ft()
# 
#        prot = ftrot.get_polar_t()
#        prot.show_image()
#        plt.show()  
#
#        prot.save(testfolder + "prot.png")    
#    
#        # fft correlation between im and prot
#        protft = ImgFFT(prot)
#        protft.ft()
#        
#        
#        corr = imft.correlate(ftrot)
#        corr.save(testfolder + "corrcorr.png")
#        dx,dy = corr.find_translation(1)
#        
#        corr.show_image()
#        a = corr.show_translation(dx, dy)
#        tsx.append(a[0])
#        tsy.append(a[1])
#    
#        print(dx, dy)  
#        
#        dx = float(dx)
#        dy = float(dy)
#        angle = np.sqrt(dx*dx + dy*dy)
#        print(angle)  
#        print("---------Angle: ", i,"----------")
#    plt.show()
#    
#    plt.plot(tsx, tsy, 'ro')
#    plt.show()
#    re = ft.resize_image(100, 100)
#    re.show_image()
#    plt.show()
    