# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:44:04 2017

@author: Mauro
"""

#==============================================================================
# Define Imports
#==============================================================================

# TkInter
from Tkinter import Tk, PhotoImage, Label 

# sys imports
from os import mkdir 
from os.path import join, split, isdir
from shutil import rmtree

# matlibplot imports
import matplotlib.pyplot as plt

# my imports
from MyImage_class import MyImage

class ImagePath:
    
    def __init__(self, name, image):
        self.image = image
        self.name = name


class CrossCorrGUI:
    
    def __init__(self, imagepathname):
        
        proc_path, ext = split(imagepathname)
        path, name = split(proc_path)
        self.mainpath = path
        self.name = name
        self.inimg_name = join(self.name, ext)
        
        
        # create the directory for the elaboration
        self.bufpath = join(self.path,self.name)
        if not isdir(self.bufpath):
            mkdir(self.bufpath)
        
        # open the source image
        self.inimage = ImagePath(self.name, MyImage())
        self.inimage.image.read_from_file(self.inimage.path)
    
    def savegif(self,imagepath):
        plt.imsave(self.bufpath + imagepath + '.gif', imagepath.image.data, format = "gif")
        
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

if __name__ == "__name__":
    
    img_path = "C://Users/Mauro/Desktop/Vita Online/Programming/Picture cross corr/silentcam/dataset24/avg/correlation_images/corr_1497777846958.png"
    m = CrossCorrGUI(img_path)
    
    
    root = Tk()
    logo = PhotoImage(file="../images/python_logo_small.gif")
    w = Label(root, 
          compound = Tk.CENTER,
          text="WHAT THE FUCK TKINTER", 
          image=logo).pack(side="right")

    root.mainloop()