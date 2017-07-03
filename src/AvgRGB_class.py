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
        algimg.limit(1.0)
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
        
#        self.avg.transpose()
#        self.avg.rotate(90)

       
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

            algimage.rotate(self.algs[i][2])
            
            algimage.move(-self.algs[i][0], -self.algs[i][1])
            
            algimage.rotate(-90)
            
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
        for i, img in enumerate(self.imgs):          
            img.squareit()
            self.imgs.set_image(i,img)
        lg.info("dataset squared")
 
    def transpose(self):
        for i, img in enumerate(self.imgs):
            img.transpose()
            self.imgs.set_image(i,img)
        lg.info("dataset transposed")
        
    def normalize(self):
        for i, img in enumerate(self.imgs):
            img.normalize()
            self.imgs.set_image(i,img)
        lg.info("dataset normalized")
    
    def binning(self, n = 1):
        for i, img in enumerate(self.imgs):
            img.binning(n)
            self.imgs.set_image(i,img)
        lg.info("dataset binned {0} times".format(n))
    

        
if __name__ == "__main__":
    
#    from matplotlib import pyplot as plt
#    
#    sound = True
#    
#    testdatasetpath = "../../../silentcam/rgbtestdataset/"
#    template_folder = join(testdatasetpath, "template_folder")
#
#    if not isdir(testdatasetpath):
#        mkdir(testdatasetpath)  
#    
#    logpathdir = join(testdatasetpath, "tlog")
#    if not isdir(logpathdir):
#        mkdir(logpathdir)    
#    
#    # create a test dataset:
#    mypicname = "../../../volpe-test_2.png"
#    mypic = MyRGBImg()
#    mypic.read_from_file(mypicname)
#       
#    if not isdir(template_folder):
#        mkdir(template_folder)
#        
#    mypic.save(join(template_folder, "template.png"))
#    
#    mypic.show_image()
#    plt.show()
#
#    print("------------------------------")
#    print("creating dataset")
#    print("------------------------------")   
#
#    np.random.seed(5)
#    datasetangles = []
#    datasetshifts = []
#    
#    datatrans = []
#
#    
#    with open(join(logpathdir, "mytransformations.log"), 'w') as f:
#        for i in range(10):
#            image = deepcopy(mypic)
#           
#            anglefirst = False if np.random.randint(0,2) == 0 else True
#            angle = np.random.randint(-10, 10)
#            dx = np.random.randint(-50, 50)
#            dy = np.random.randint(-50, 50)
#            
#            f.write("{0} {1} {2} {3}\n".format(anglefirst, angle, dx, dy))
#            
#            
#            datatrans.append((anglefirst, angle, dx, dy))
#            
#            if anglefirst:
#                datasetangles.append(angle)
#                image.rotate(angle)
#    
#                datasetshifts.append((dx,dy))
#                image.move(dx, dy)
#            else:
#                datasetshifts.append((dx,dy))
#                image.move(dx, dy) 
#    
#                datasetangles.append(angle)
#                image.rotate(angle)
#            
#            print(datatrans[i])
#               
#            image.show_image()
#            plt.show()
#            
#            image.save(join(testdatasetpath, "pic_" + str(i) + ".png"))     
#    

    pathtodataset = "../../../silentcam/dataset41/"

    from LogTimes import TimingsTot
    
    t = TimingsTot(pathtodataset + "rgb_time_logfile.log")
    
    avg = AvgRGB_savememory(pathtodataset)
    avg.gather_pictures_names()
    t.log("Loaded names")
    avg.load_algs()
    t.log("Loaded aligments")
    avg.align_images(debug = True)
    t.log("Aligned Images")
    avg.average(aligned = True, debug = True)
    t.log("Averaged Images")
    avg.save_avg()
    
    import winsound
    Freq = 2500 # Set Frequency To 2500 Hertz
    Dur = 1000 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)
