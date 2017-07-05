# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:33:12 2017

@author: Mauro

This class manages gray scale images. The images are stored as mxn arrays and 
the class provide basic processing metods
"""

#==============================================================================
# # Imports
#==============================================================================

# numpy import
import numpy as np

# matplotlib import
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# scipy import
from scipy import signal

# py imports
from copy import deepcopy

#==============================================================================
# # Image Handling class
#==============================================================================

class MyImage(object):
    ''' Main class, this will be a standard image object mxn matrix of values'''
    
    # ------ initialization functions ------
    
    def __init__(self, data = np.zeros((5,5))):  
        ''' The image can be initiated with any numpy array, default is a 5x5 
        zeroed matrix. The image can be intiated by tuple indicating its size
        (mxn). The image can be initiated by a path to an image.
        The data is stored in the self data folder.
        Usage:
            img = MyImg()
            img = MyImg(np.zeros((512, 512)))
            img = MyImg((512, 512))
            img = MyImg(path/to/picture.png)
        '''
        if type(data) == np.ndarray:
            self.data = data
        elif type(data) == tuple:
            if len(data) == 2:
                self.data = np.zeros(data)
        elif type(data) == str:
            # shall i check for path being an image?
            self.read_from_file(data)
        else:
            raise ValueError("data type not supported")
            
    
    # ------ debug options ------
    
    def inspect(self, output = True):
        ''' short function that returns the image values: mean,
        standard deviation, max, min and size of image
        if output is True, it prints to the console the string containing the 
        formatted value
        ''' 
        m = np.mean(self.data)
        s = np.std(self.data)
        u = np.max(self.data)
        l = np.min(self.data)
        d = self.data.shape
        
        if output:
            s  = "Mean: {0:.2f} | Std: {1:.2f} | Max: {2:.2f}|Min: {3:.2f} | \
                  Dim: {4[0]}x{4[1]}".format(m, s, u, l, d)
            print(s)
            return s
            
        return (m, s, u, l, d)   
    
    def show_image(self):
        ''' This prepares a image canvas for matlibplot visible in  the 
        IPython console.
        '''
        data = deepcopy(self.data)  # copy the data to not modify them
        
        # limit the data between 0 and 1
        mi = np.min(data)
        pospic = data + mi
        m = np.max(pospic)
        npic = pospic / float(m)
        data = 1 - npic 
        
        # show the image in greyscale
        plt.imshow(data, cmap = "Greys")    
    
    def get_size(self):
        return (self.data.shape[0], self.data.shape[1])
    
    def get_sizex(self):
        return self.get_size()[0]
    
    def get_sizey(self):
        return self.get_size()[1]
    
    # ------ I/O functions ------
    
    def read_from_file(self, filepathname):
        ''' import image from file using the mpimg utility of matplotlib'''
        # todo warnings about file existing ?
        self.data = mpimg.imread(filepathname)

    def save(self, filename):
        ''' saves an image using the pyplot method'''
        plt.imsave(filename, self.data)    


    # ------ operators overload  ------       
    def __add__(self, rhs):
        ''' sums two images px by px'''
        self.data = self.data + rhs.data
        return MyImage(self.data)
    
    def __truediv__(self, rhs):
        ''' divide image by scalar (myimg / number)'''
        rpic = deepcopy(self.data)
        for x in range(self.data.shape[0]):
            for y in range(self.data.shape[1]):
                rpic[x][y] = self.data[x][y] / rhs
        
        return MyImage(rpic)

    # ------ editing functions ------
    def create_composite_right(self, rhsimage):
        ''' concatenates 2 images on the right'''
        # todo multiple arugments
        # enlarge the array to fit the next image
        self.data = np.concatenate((self.data, rhsimage.data), axis = 1)
    
    def normalize(self):
        ''' normalize the picture values so that the resulting image will have
        mean = 0 and std = 1'''
        m = np.mean(self.data)
        s = np.std(self.data)
        self.data = (self.data - m) / s

    def convert2grayscale(self):
        ''' when importing an rgb image is necessary to calculate the
        luminosity and reduce the array from mxnx3 to mxn
        '''
        self.data = np.dot(self.data[...,:3], [0.299, 0.587, 0.114])
    
    def transpose(self):
        ''' transposes the picture from mxn to nxm'''
        self.data.transpose()
        
    def binning(self, n = 1):
        ''' Averages a matrix of 2x2 pixels to one value, effectively reducing
        size by two and averaging the value, giving less noise. n indicates
        how many time the procedure is done 
        512x512 bin 1 -> 256x256 bin 2 -> 128128 bin 3 -> ...
        '''
        for i in range(n):
            # initialize resulting image
            rimg = np.zeros( (int(self.data.shape[0] / 2) , int(self.data.shape[1] / 2)))
            
            # calculate for each pixel the corresponding
            # idx rimg = 2*idx srcimg
            for x in range(rimg.shape[0]):
                for y in range(rimg.shape[1]):
                    a = self.data[x*2]    [y*2]
                    b = self.data[x*2 + 1][y*2]
                    c = self.data[x*2]    [y*2 + 1]
                    d = self.data[x*2 + 1][y*2 + 1]
                    rimg[x][y] =  (a + b + c + d) / 4.0
            
            self.data = rimg

    def move(self, dx, dy):
        ''' moves the picture by the dx or dy values. dx dy must be ints'''
        # correction to give dx a right movement if positive
        dx = -dx
        
        # initialize the image
        mpic = np.zeros(self.data.shape)
        
        # get image size
        sizex = mpic.shape[0]
        sizey = mpic.shape[1]
        
        for x in range(sizex):
            for y in range(sizey):
                xdx = x + dx
                ydy = y + dy
                if xdx >= 0 and xdx < sizex and ydy >= 0 and ydy < sizey:
                    mpic[x][y] = self.data[xdx][ydy]
        
        self.data = mpic
    
    def squareit(self, mode = "center"):
        ''' Squares the image. Two methods available 
        center: cuts a square in the center of the picture
        left side: cuts a square on top or on left side of the pic
        '''
        if mode == "center":
            lx = self.data.shape[0]
            ly = self.data.shape[1]
            
            if lx > ly:
                ix = int(lx / 2 - ly / 2)
                iy = int(lx / 2 + ly / 2)
                self.data = self.data[ ix : iy , 0 : ly]
            else:
                ix = int(ly / 2 - lx / 2)
                iy = int(ly / 2 + lx / 2)
                self.data = self.data[0 : lx, ix : iy ]            
        if mode == "left side":
            lx = self.data.shape[0]
            ly = self.data.shape[1]
            
            if lx > ly:
                self.data = self.data[0:ly,0:ly]
            else:
                self.data = self.data[0:lx,0:lx]
    
    def correlate(self, image):
        ''' scipy correlate function. veri slow, based on convolution'''
        corr = signal.correlate2d(image.data, self.data, boundary='symm', mode='same')
        return Corr(corr)

    def limit(self, valmax):
        ''' remaps the values from 0 to valmax'''
        # si potrebbe cambiare da minvalue a value
        mi = self.data.min()
        mi = np.abs(mi)
        pospic = self.data + mi
        m = np.max(pospic)
        npic = pospic / float(m)
        self.data = npic * valmax
    
    def apply_mask(self, mask):
        ''' apply a mask on the picture with a dot product '''
        self.data = self.data * mask.data
        
    def rotate(self, deg, center = (0,0)):
        ''' rotates the image by set degree'''
        #where c is the cosine of the angle, s is the sine of the angle and
        #x0, y0 are used to correctly translate the rotated image.
        
        # size of source image
        src_dimsx = self.data.shape[0]
        src_dimsy = self.data.shape[1]
        
        # get the radians and calculate sin and cos
        rad = np.deg2rad(deg)
        c = np.cos(rad)
        s = np.sin(rad)
        
        # calculate center of image
        cx = center[0] + src_dimsx/2
        cy = center[1] + src_dimsy/2
        
        # factor that moves the index to the center
        x0 = cx - c*cx - s*cx
        y0 = cy - c*cy + s*cy
        
        # initialize destination image
        dest = MyImage(self.data.shape)
        for y in range(src_dimsy):
            for x in range(src_dimsx):
                # get the source indexes
                src_x = int(c*x + s*y + x0)
                src_y = int(-s*x + c*y + y0)
                if src_y > 0 and src_y < src_dimsy and src_x > 0 and src_x < src_dimsx:
                    #paste the value in the destination image
                    dest.data[x][y] = self.data[src_x][src_y]
                    
        self.data = dest.data

#==============================================================================
# # Cross correlation image Handling class
#==============================================================================

class Corr(MyImage):
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
        for x in range(self.data.shape[0] - msize):
            for y in range(self.data.shape[1] - msize):
                # calculate mean of the matrix
                s = 0
                for i in range(msize):
                    for j in range(msize):
                        s += self.data[x + i][y + j]
                s =  s / float(msize)**2
                
                # assign the best value to best, the return tuple
                if s > best[0]:
                    best = (s, x, y)
        return best
    
    def find_translation(self, peak):
        ''' converts the peak into the translation needed to overlap completely
        the pictures
        '''
        if type(peak) == int:
            peak = self.find_peak(peak)
        
        #best = self.find_peak(msize)
        peakx = peak[1]
        peaky = peak[2]
        
        dx = -(self.data.shape[0]/2 - peakx)
        dy = self.data.shape[1]/2 - peaky
        
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
        ody = dx + self.data.shape[0]/2
        odx = self.data.shape[1]/2 - dy
        plt.scatter(odx, ody, s=40, alpha = .5)    
        return odx, ody

#==============================================================================
# # Mask image Handling class
#==============================================================================

class Mask(MyImage):
    ''' This class manages the creation of masks
    '''
    
    def create_circle_mask(self, radius, smooth):
        ''' creates a smoothed circle with value 1 in the center and zero
        outside radius + smooth, uses a linear interpolation from 0 to 1 in 
        r +- smooth.
        '''
        # initialize data array
        dims = self.data.shape
        mask = np.ones(dims)*0.5
        center = (dims[0]/2.0, dims[1]/2.0)
        for i in range(dims[0]):
            for j in range(dims[1]):
                # if distance from center > r + s = 0, < r - s = 1 else 
                # smooth interpolate
                dcenter = np.sqrt( (i - center[0])**2 + (j - center[1])**2)
                if dcenter >= (radius + smooth):
                    mask[i][j] = 0
                elif dcenter <= (radius - smooth):
                    mask[i][j] = 1
                else:
                    y = -1*(dcenter - (radius + smooth))/radius
                    mask[i][j] = y
        self.data = mask
        
        # normalize the picture from 0 to 1
        self.limit(1) 
        return self.data
    
    def invert(self):
        self.data = 1 - self.data 
    
    def bandpass(self, rin, sin, rout, sout):
        ''' To create a band pass two circle images are created, one inverted
        and pasted into dthe other'''
        
        # if radius zero dont create the inner circle
        if rin != 0:
            self.create_circle_mask(rin, sin)
        else:
            self.data = np.zeros(self.data.shape)
        
        # create the outer circle
        bigcircle = deepcopy(self)
        bigcircle.create_circle_mask(rout, sout)
        bigcircle.invert() 
        
        # sum the two pictures
        m = (self + bigcircle)
        
        # limit fro 0 to 1 and invert 
        m.limit(1)
        m.invert()  
        
        self.data = m.data
    
    def __add__(self, rhs):
        ''' overload of the + operator why is not inherited from MyImage?'''
        
        self.data = self.data + rhs.data
        return Mask(self.data)
    
    
if __name__ == "__main__":
    mypicname = "../../../images.png"
    mypic = MyImage()
    mypic.read_from_file(mypicname)
    mypic.squareit()
    mypic.convert2grayscale()
    mypic.binning(0)
    mypic.normalize()
    
    mypic.show_image()
    plt.show()
    
    movpic = deepcopy(mypic)
    movpic.move(100, 0)
    
    movpic.show_image()
    plt.show()
    
    myrot = deepcopy(mypic)
    myrot.rotate(45, center = (0, 0))
    myrot.normalize()
    
    myrot.show_image()
    plt.show()  
    
    
    # at theoretical level the precision can be to the 100th of degree...
#    angles = [10, 29.999, 30, 30.001]
#    myrots = []
#    for angle in angles:
#        myrot10 = deepcopy(mypic)
#        myrot10.rotate(angle)
#        myrot10.normalize()
#        myrot10.show_image()
#        plt.show()
#        myrots.append(myrot10)
#
#    from ImageFFT_class import ImgFFT
#    myrotft = ImgFFT(myrot)
#    myrotft.ft()
#    smax = 0
#    for i, rot in enumerate(myrots):
#        # find rotation
#        
#        rotft = ImgFFT(rot)
#        rotft.ft()       
#        cc = myrotft.correlate(rotft)
#        cc.show_image()
#        s, dx, dy = cc.find_peak(1)
#        plt.show()
#        print("my angle:", angles[i])
#        print(dx, dy, s)
#    
#    xarr = [i * 10 + 10 for i in range(20)]
#    yarr = [np.rad2deg(1 / float(x)) for x in xarr]    
#        
#    plt.scatter(xarr, yarr)
#    plt.show()
    
#    # test the average
#    from ImageFFT_class import ImgFFT
#    
#    # lena is the template
#    template = deepcopy(mypic)
#    tempft = ImgFFT(template)
#    tempft.ft()
#    
#    # construct a rotation space for the template
#    rotangles = [x for x in range(-10,10,1)]
#    
#    rotationspace = []
##    for angle in rotangles:
##        print("rotating template angle:", angle)
##        temprot = deepcopy(template)
##        temprot.rotate(angle)
##        temprotft = ImgFFT(temprot)
##        temprotft.ft()
##        rotationspace.append(temprotft)
#    
#    # construct a dataset with randomly moved and rotated images
#    
#    np.random.seed(5)
#    dataset = []
#    datasetangles = []
#    datasetshifts = []
#    
#    datatrans = []
#    
#    print("------------------------------")
#    print("creating dataset")
#    print("------------------------------")
#
#    angle_list = np.arange(-20, 20, 5)    
#    for i, ngle in enumerate(angle_list):
#        image = deepcopy(mypic)
#        anglefirst = False if np.random.randint(0,2) == 0 else True
#        
##        angle = np.random.randint(-10, 10)
##        dx = np.random.randint(-50, 50)
##        dy = np.random.randint(-50, 50)
#
#        anglefirst = True
#        angle = angle_list[i]
#        print(angle)
#        dx = 0
#        dy = 0
#        
#        datatrans.append((anglefirst, angle, dx, dy))
#        
#        if anglefirst:
#            datasetangles.append(angle)
#            image.rotate(angle)
#
#            datasetshifts.append((dx,dy))
#            image.move(dx, dy)
#        else:
#            datasetshifts.append((dx,dy))
#            image.move(dx, dy) 
#
#            datasetangles.append(angle)
#            image.rotate(angle)
#        
#        print(datatrans[i])
#           
#        image.show_image()
#        plt.show()
#        dataset.append(image)
#    
#    # for each image test the rotation against the template
#    print("------------------------------")
#    print("Align dataset")
#    print("------------------------------")  
#    
#    def distance(x, y):
#        d = np.sqrt((y-x)**2)
#        return d
#    
#    algimg = []
#    for i, image in enumerate(dataset):
#        print("original transformation: ", datatrans[i])
#        imageft = ImgFFT(image)
#        imageft.ft()
#
##        smax = 0
##        idxmax = 0
##        for idx, temp in enumerate(rotationspace):
##            corr = temp.correlate(imageft)
##            s, dx, dy = corr.find_peak(1)
##            
##            
##            
##            if s > smax:
##                smax = s
##                idxmax = idx
##        
##        print("angle found",rotangles[idxmax] )
#        
#        rotalgimage = deepcopy(image)
##        rotalgimage.rotate(-rotangles[idxmax])
#        
#        rotalgimageft = ImgFFT(rotalgimage)
#        rotalgimageft.ft()
#        
#        corr = rotalgimageft.correlate(tempft)
#        
#
#        
#        dx, dy = corr.find_translation(1)
#
#        corr.show_image()
#        corr.show_translation(dx, dy)
#        plt.show()
#        
#        print("shifts:", dx, dy)
#        
#        rotalgimage.move(dx, dy)
#        # distance
##        print("distance")
##        print(distance(datatrans[i][1], rotangles[idxmax]),
##              distance(datatrans[i][2], -dx),
##              distance(datatrans[i][3], -dy)
##              )        
##        
#        rotalgimage.show_image()
#        plt.show()
#        algimg.append(rotalgimage)
        

        
        
            
            
            
    
    # then rotate it and test the shifts
    
    
    
    # test correlation
#    cc = mypic.correlate(movpic)
#    
#    cc.show_image()
#    
#    dx, dy = cc.find_translation()
#    cc.show_translation(dx, dy)
#    plt.show()
    
#    mypic.create_composite_right(movpic)
#
#    mypic.show_image()
#    plt.show()
#    
    