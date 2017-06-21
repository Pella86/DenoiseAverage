# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:44:04 2017

@author: Mauro
"""

#==============================================================================
# Define Imports
#==============================================================================

# TkInter
from tkinter import Tk, PhotoImage, Label, Frame

# sys imports
from os import mkdir 
from os.path import join, split, isdir, isfile, splitext
from shutil import rmtree

# matlibplot imports
import matplotlib.pyplot as plt
from scipy.misc import imsave

# my imports
from MyImage_class import MyImage



def get_pathname(path):
        path, nameext = split(path)
        name, ext = splitext(nameext)
        return path, name, ext

class CrossCorrGUI:
    
    def __init__(self, imagepathname):
        
        path, name, ext = get_pathname(imagepathname)
        self.mainpath = path
        self.name = name
        self.inimg_name = self.name + ext
        
        
        
        # create the directory for the elaboration
        self.bufpath = join(self.mainpath,self.name)
        if not isdir(self.bufpath):
            mkdir(self.bufpath)
        
        bufpath = self.bufpath
            
        class ImagePath:
    
            def __init__(self, name, image):
                self.image = image
                self.name = name
                self.gifname = join(bufpath, self.name) + '.gif'
        
        # open the source image
        self.inimage = ImagePath(self.name, MyImage())
        self.inimage.image.read_from_file(imagepathname)
        
        self.savegif(self.inimage)
    
    def savegif(self,imagepath):
        imsave(imagepath.gifname, imagepath.image.data, format = "gif")
        
    def rm(self):
        rmtree(self.bufpath)
        
        # save the image in the buffer as 
        
        # get the fourier transform done
        
        # get the powerspectrum done
        
        # save ps as gif
        
        # make the mask
        
        # save the mask
        
        # apply mask on fourier
        
        # inverse fft

if __name__ == "__main__":
    
    img_path = "C:/Users/Mauro/Desktop/Vita Online/Programming/Picture cross corr/silentcam/dataset24/avg/correlation_images/corr_1497777846958.png"
    
    
    m = CrossCorrGUI(img_path)
    print(isfile(m.inimage.gifname))
    root = Tk()
    logo = PhotoImage(file = m.inimage.gifname)
    print(logo)
    frame = Frame(root, width = 100, height = 100)
    frame.pack()
    w = Label(frame,
          text="WHAT THE FUCK TKINTER", image = logo)
    w.pack(side = "left")

    root.mainloop()