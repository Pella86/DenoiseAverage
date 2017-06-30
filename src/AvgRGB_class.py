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
from os.path import isdir, isfile, join, splitext, split
from os import listdir, mkdir
import logging as lg
from copy import deepcopy

# My imports
from MyRGBImage_class import MyRGBImg


        
def get_pathname(path):
    ''' Little function to split the path in path, name, extension'''
    path, nameext = split(path)
    name, ext = splitext(nameext)
    return path, name, ext 


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
            path, name, ext = get_pathname(imgname)
            if ext in ['.png', '.jpg']:
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


class AvgRGB_savememory(object):
    
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
        lg.basicConfig(filename=join(self.avgpath,'rgb_average_savemem.log'),level=lg.INFO)
        
        
        # instead of loading all the pictures in one array
        # create a path array that reads the pictures at will
        
        self.imgs_names = []
        self.avg = MyRGBImg()
        self.algs = []
        
    
    def get_image(self, index):
        # read the image corresponding to the path
        pathtopic = join(self.path, self.imgs_names[index])
        myimg = MyRGBImg()
        myimg.read_from_file(pathtopic)
        return myimg
    
    def get_alg_image(self, index):
        filename, ext = splitext(self.imgs_names[index])
        pathtopic = join(self.subfolders["aligned_rgb_images"], ("alg_" + filename + ".png" ))
        myimg = MyRGBImg()
        myimg.read_from_file(pathtopic)
        return myimg       
    
    def save_alg_image(self, index, algimg):
        filename, ext = splitext(self.imgs_names[index])
        algimg.save(join(self.subfolders["aligned_rgb_images"], ("alg_" + filename + ".png" )))        
    
    def gather_pictures_names(self):
        # for now gathe all the files, next check for picture extensions
        p = self.path
        
        filenames = [f for f in listdir(p) if isfile(join(p, f))]
        for filename in filenames:
            path, name, ext = get_pathname(filename)
            if ext in ['.png', '.jpg']:       
                self.imgs_names.append(filename)

    def average(self, aligned = True, debug = False):
        sizedataset = len(self.imgs_names)
        if aligned:
            picture = self.get_alg_image(0)
        else:
            picture = self.get_image(0)       
        
        s = MyRGBImg(np.zeros(picture.data.shape))
        s = color.rgb2lab(s.data)
        
        for i in range(sizedataset):
            if debug:
                print("Averaging image: " , i)
            #load the picture
            if aligned:
                picture = self.get_alg_image(i)
            else:
                picture = self.get_image(i)
            # convert both to lab
            im = color.rgb2lab(picture.data)

            #perform operations
            s += im 
            
        s = s / float(sizedataset)
        self.avg = MyRGBImg(color.lab2rgb(s))
        self.avg.transpose()
        self.avg.rotate(90)
       
    def load_algs(self):
        with open(join(self.subfolders["results"], "shifts_log.txt")) as f:
            lines = f.readlines()
        
        self.algs = []
        for line in lines:
            sdata = line.split(' | ')
            sdata = [d.strip() for d in sdata]
            data = [int(sdata[0]), int(sdata[1]), float(sdata[2])]
            self.algs.append(data)
        lg.info("Alignments imported successfully")
        
    def align_images(self, debug = False):
        self.algimgs = []
        for i in range(len(self.imgs_names)):
            if debug:
                print("Aligning image:", i)
                print("algs:", self.algs[i])
            
            # load picture to align
            algimage = self.get_image(i)
            
            algimage.squareit()

            rotalg = True
            if rotalg:
                algimage.rotate(-self.algs[i][2])
            
            algimage.move(-self.algs[i][0], -self.algs[i][1])
            
            # save the image
            self.save_alg_image(i, algimage)
            
        lg.info("Images aligned successfully")

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
    
    pathtodataset = "../../../silentcam/dataset34/"
    
#    avg = AvgRGB(pathtodataset)
#    avg.gather_pictures()
#    avg.load_algs()
#    avg.align_images()
#    avg.average()
#    avg.save_avg()
    from LogTimes import TimingsTot
    
    t = TimingsTot(pathtodataset + "time_logfile.log")
    
    avg = AvgRGB_savememory(pathtodataset)
    avg.gather_pictures_names()
    t.logtimestr("Loaded names")
    avg.load_algs()
    t.logtimestr("Loaded aligments")
    avg.align_images(debug = True)
    t.logtimestr("Aligned Images")
    avg.average(aligned = True, debug = True)
    t.logtimestr("Averaged Images")
    avg.save_avg()
    
    import winsound
    Freq = 2500 # Set Frequency To 2500 Hertz
    Dur = 1000 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)
