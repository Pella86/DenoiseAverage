# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:24:18 2017

@author: Mauro
"""

# This module deals with the Average of RGB images
# no correlation yet

#==============================================================================
# Define Imports
#==============================================================================

# numpy import
import numpy as np
from skimage import color


# py imports
from os.path import isdir, isfile, join, splitext
from os import listdir, mkdir
import logging as lg

# My imports
from MyRGBImage_class import MyRGBImg


class AvgRGB(object):
    
    # initialize method
    def __init__(self, path):
        # define main path
        self.path = path
        
        # folder environment
        self.avgpath = ""
        self.subfolders = {}

        try:
            self.makeavgdir()
        except FileNotFoundError as e:
            print("Folder not found")
        except:
            print("WTF")        

        # create log file in the avg folder
        lg.basicConfig(filename=join(self.avgpath,'rgb_average.log'),level=lg.INFO)
        
        
        self.imgs = []
        self.avg = MyRGBImg()
        self.algs = []
        self.algimgs = []
        
        
    
    def gather_pictures(self):
        # for now gathe all the files, next check for picture extensions
        p = self.path
        self.names = [f for f in listdir(p) if isfile(join(p, f))]
        
        for imgname in self.names:
            imagepath = join(self.path, imgname)
            img = MyRGBImg()
            img.read_from_file(imagepath)
            self.imgs.append(img)
            lg.info("Image: {0} imported successfully".format(imagepath))

    def average(self, aligned = True):
        if aligned:
            dataset = self.algimgs
        else:
            dataset = self.imgs
        
        s = MyRGBImg(np.zeros(dataset[0].data.shape))
        s = color.rgb2lab(s.data)
        for i, picture in enumerate(dataset):
            print("Averaging image: " , i)
            # convert both to lab
            im = color.rgb2lab(picture.data)
            #perform operations
            s += im 
            
        s = s / float(len(dataset))
        self.avg = MyRGBImg(color.lab2rgb(s))
 

#    def average(self, aligned = True):
#        if aligned:
#            dataset = self.algimgs
#        else:
#            dataset = self.imgs
#        s = MyRGBImg(np.zeros(dataset[0].data.shape))
#        for i, picture in enumerate(dataset):
#            print("Averaging image: " , i)
#            # convert both to lab
#            sin = color.rgb2lab(s.data)
#            im = color.rgb2lab(picture.data)
#            #perform operations
#            m = sin + im  
#            print(m[0][0][0])
#            m = m / float(2)
#            
#            #convert back
#            s.data = color.lab2rgb(m)
#  
#        self.avg = s
#        
       
    def load_algs(self):
        with open(join(self.subfolders["results"], "shifts_log.txt")) as f:
            lines = f.readlines()
        
        self.algs = []
        for line in lines:
            data = line.split(' | ')
            data = [int(d.strip()) for d in data]
            self.algs.append(data)
        lg.info("Alignments imported successfully")
        
    def align_images(self):
        self.algimgs = []
        for i, image in enumerate(self.imgs):
            algimage = deepcopy(image)
            print("alg:", self.algs[i][0], self.algs[i][1])
            algimage.move(-self.algs[i][1], -self.algs[i][0])
            self.algimgs.append(algimage)
        lg.info("Images aligned successfully")
            
    def save_algimgs(self):
        for i, algimg in enumerate(self.algimgs):
            filename, ext = splitext(self.names[i])
            algimg.save(join(self.subfolders["aligned_rgb_images"], ("alg_" + filename + ".png" )))
        lg.info("Saved aligned images successfully") 
    
    def save_avg(self, name = "avg_rgb.png"):
        self.avg.save(join(self.subfolders["results"], name))
            
    def makeavgdir(self):
        # create a folder average into the dataset path
        # avg
        #  |- processed_images
        #  |- aligned_images
        #  |- correlation_images
        #  |- results
        #  |- aligned_rgb_images
        self.avgpath = join(self.path, "avg")
        if not isdir(self.avgpath):
            mkdir(self.avgpath)
        
        subfolders = ["aligned_rgb_images", "results"]
        for folder in subfolders:
            self.subfolders[folder] = join(self.avgpath, folder)
            if not isdir(self.subfolders[folder]):
                mkdir(self.subfolders[folder])    

    

if __name__ == "__main__":
    
    pathtodataset = "../../silentcam/dataset25/"
    
    avg = AvgRGB(pathtodataset)
    avg.gather_pictures()
    avg.load_algs()
    avg.align_images()
    avg.average()
    avg.save_avg()
    
    import winsound
    Freq = 2500 # Set Frequency To 2500 Hertz
    Dur = 1000 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)
