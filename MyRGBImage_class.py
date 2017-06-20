# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:24:50 2017

@author: Mauro
"""

class MyRGBImg(object):

    def __init__(self, data = np.zeros((5,5,3)) ):
        self.data = data
     
    def read_from_file(self, filepathname):
        # import image from file
        # todo warnings about file existing
        self.data = mpimg.imread(filepathname)
    
    def get_channel(self, channel):
        c2idx ={'r':0, 'g':1, 'b':2}
        return MyImage(255 - self.data[:,:,c2idx[channel]].transpose())
    
    def set_channel(self, image, channel):
        c2idx ={'r':0, 'g':1, 'b':2}
        img = 255 - image.data
        self.data[:,:,c2idx[channel]] = img.transpose()
        
    
    def show_image(self):
        plt.imshow(self.data)
    
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
                        mpic[x][y][c] = int(255 - self.data[xdx][ydy][c])
                        if mpic[x][y][c] <= 0:
                            mpic[x][y][c] = 0
                        if mpic[x][y][c] >= 255:
                            mpic[x][y][c] = 255
        self.data = mpic
        
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

    def limit(self, valmax):
        mi = np.min(self.data)
        pospic = self.data + mi
        m = np.max(pospic)
        if m == 0:
            npic = pospic / float(m)
            self.data = npic * valmax
    
    def save(self, filename):
        plt.imsave(filename, self.data)
            
    
