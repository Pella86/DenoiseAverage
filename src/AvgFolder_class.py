# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 06:44:03 2017

@author: Mauro
"""

# This module deals with the Average

# Define Imports

# numpy import
import numpy as np

# py imports
from os.path import isdir, isfile, join, splitext
from os import listdir, mkdir
from copy import deepcopy
import logging as lg

# My imports
from MyImage_class import MyImage
from ImageFFT_class import ImgFFT

#==============================================================================
# Exceptions
#==============================================================================

class TemplateTypeError(Exception):
   def __init__(self, value):
       self.value = value
   def __str__(self):
       return "Wrong template type: " + repr(self.value)

#==============================================================================
# Class 
#==============================================================================

class AvgFolder(object):
    
    # Initialization functions
    def __init__(self, path):
        # define the main path
        self.path = path
        
        # folder environment variable
        self.names = []
        self.avgpath = ""
        self.subfolders = {}
        
        # create the folder environment
        try:
            self.makeavgdir()
        except FileNotFoundError as e:
            print("Folder not found")
        except:
            print("WTF")
            
        # create log file in the avg folder
        lg.basicConfig(filename=join(self.avgpath,'example.log'),level=lg.INFO)
        
        # initialize variables
        self.imgs = []
        self.template = MyImage()
        self.templateft = 0
               
        self.algimgs = []
        self.corrs = []
        self.shifts = []
        
        self.avg = MyImage()
        
    
    def gather_pictures(self):
        # for now gather all the files, next check for picture extensions
        p = self.path
        self.names = [f for f in listdir(p) if isfile(join(p, f))]

        for imgname in self.names:
            imagepath = join(self.path, imgname)
            img = MyImage()
            img.read_from_file(imagepath)
            self.imgs.append(img)
            lg.info("Image: {0} imported successfully".format(imagepath))

    def makeavgdir(self):
        # create a folder average into the dataset path
        # avg
        #  |- processed_images
        #  |- aligned_images
        #  |- correlation_images
        #  |- results
        self.avgpath = join(self.path, "avg")
        if not isdir(self.avgpath):
            mkdir(self.avgpath)
        
        subfolders = ["processed_images", "aligned_images", 
                      "correlation_images", "results"]
        for folder in subfolders:
            self.subfolders[folder] = join(self.avgpath, folder)
            if not isdir(self.subfolders[folder]):
                mkdir(self.subfolders[folder])    

    
    # image operations
    def c2gscale(self):
        for img in self.imgs:
            img.convert2grayscale()
        lg.info("dataset converted to grayscale")
    
    def squareit(self):
        for img in self.imgs:
            img.squareit()
        lg.info("dataset squared")
 
    def transpose(self):
        for img in self.imgs:
            img.transpose()
        lg.info("dataset transposed")
        
    def normalize(self):
        for img in self.imgs:
            img.normalize()    
        lg.info("dataset normalized")
    
    def binning(self, n = 1):
        for img in self.imgs:
            img.binning(n)
        lg.info("dataset binned {0} times".format(n))
    
    # template handling
    def generate_template(self, option):
        if type(option) is str:
            if option == "UseFirstImage":
                self.template = self.imgs[0]
                self.templateft = ImgFFT(self.template)
                self.templateft.ft()
            elif option == "Average":
                self.average(False)
                self.template = self.avg
                self.templateft = ImgFFT(self.template)
                self.templateft.ft()
            else:
                raise TemplateTypeError(option)
        elif type(option) == MyImage:
            self.template = option
            self.templateft = ImgFFT(self.template)
            self.templateft.ft()
        else:
           raise TemplateTypeError(type(option))
        lg.info("template created: {0}".format(option))

    
    def align_images(self, debug = False):
        c = 0
        for image in self.imgs:

            imgft = ImgFFT(image)
            imgft.ft()
            
            corr = imgft.correlate(self.templateft)
            self.corrs.append(corr)
            dx, dy = corr.find_translation(1)
            self.shifts.append((dx,dy))
            
            algimg = MyImage()
            algimg = deepcopy(image)
            algimg.move(dx,dy)
            self.algimgs.append(algimg)
            if debug:
                print("Correlate image:", c)            
            lg.info("correlated image n: " + str(c))
            
            c += 1
    
    def average(self, aligned = True):
        if aligned:
            dataset = self.algimgs
        else:
            dataset = self.imgs
        s = MyImage(np.zeros(dataset[0].data.shape))
        for picture in dataset:
            s += picture
        
        
        self.avg = s / len(dataset)
    
    # I/O methods
    def save_template(self):
        self.template.save(join(self.avgpath, "template.png"))
            
    def load_template(self, filepathname):
        self.template.read_from_file(filepathname)
    
    def save_imgs(self):
        for i, img in enumerate(self.imgs):
            filename, ext = splitext(self.names[i])
            img.save(join(self.subfolders["processed_images"], "proc_" + filename + ".png"))
        lg.info("processed dataset saved, images {0}".format(i))
    
    def laod_imgs(self):
        lg.info("Loading processed images")
        p = self.subfolders["processed_images"]
        names = [f for f in listdir(p) if isfile(join(p, f))] 
        
        self.imgs = []
        for name in names:
            img = MyImage()
            img.read_from_file(name)
            self.imgs.append(img)
            lg.info("Image: {0} imported successfully".format(name))
            
    
    def save_algimgs(self):
        for i, algimg in enumerate(self.algimgs):
            filename, ext = splitext(self.names[i])
            algimg.save(join(self.subfolders["aligned_images"], ("alg_" + filename + ".png" )))
        lg.info("aligned dataset saved, images {0}".format(i))
    
    def laod_algimgs(self):
        lg.info("Loading aligned images")  
        p = self.subfolders["aligned_images"]
        names = [f for f in listdir(p) if isfile(join(p, f))] 
        
        self.imgs = []
        for name in names:
            img = MyImage()
            img.read_from_file(name)
            self.imgs.append(img)
            lg.info("Image: {0} imported successfully".format(name))    
    
    def save_corrs(self):
        for i, corr in enumerate(self.corrs):
            filename, ext = splitext(self.names[i])
            corr.save(join(self.subfolders["correlation_images"], ("corr_" + filename + ".png" )))
        lg.info("correlations dataset saved, images {0}".format(i))

    def laod_corrs(self):
        lg.info("Loading correlation images")  
        p = self.subfolders["correlation_images"]
        names = [f for f in listdir(p) if isfile(join(p, f))] 
        
        self.imgs = []
        for name in names:
            img = MyImage()
            img.read_from_file(name)
            self.imgs.append(img)
            lg.info("Image: {0} imported successfully".format(name))    
    
    def save_avg(self):
        self.avg.save(join(self.subfolders["results"], "avg.png"))
    
    def save_shifts(self):
        with open(join(self.subfolders["results"], "shifts_log.txt"), "w") as f:
            for shift in self.shifts:
                f.write("{0[0]:d} | {0[1]:d}\n".format(shift))
        lg.info("Shifts saved")

    def load_shifts(self):
        with open(join(self.subfolders["results"], "shifts_log.txt")) as f:
            lines = f.readlines()
        
        self.shifts = []
        for line in lines:
            data = line.split(' - ')
            data = [int(d.strip()) for d in data]
            print (data)
            self.shifts.append(data)

# TO DO
# - process function with arguments
# - check if already done 


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    mypath = "../../silentcam/dataset25/"
    avg = AvgFolder(mypath)
    avg.gather_pictures()
    avg.c2gscale()
    avg.squareit()
    avg.binning(0)    
    avg.transpose()
    avg.normalize() 
    
    avg.save_imgs()

        
    avg.generate_template("UseFirstImage")
    avg.save_template()
    
    avg.template.show_image()
    plt.show()  
    
    avg.template.inspect()
    
    correlate = True
    if correlate:
        # aling dataset
        avg.align_images()
        avg.save_algimgs()
        avg.save_corrs()
        avg.save_shifts()
        
        avg.average()
        avg.save_avg()
        avg.avg.show_image()
        plt.show()