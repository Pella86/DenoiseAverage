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
from matplotlib import pyplot as plt

# py imports
from os.path import isdir, isfile, join, splitext, split
from os import listdir, mkdir
import logging as lg
from copy import deepcopy

# My imports
from MyRGBImage_class import MyRGBImg
from LogTimes import Logger


        
def get_pathname(path):
    ''' Little function to split the path in path, name, extension'''
    path, nameext = split(path)
    name, ext = splitext(nameext)
    return path, name, ext 


class AvgRGB(object):
    ''' The only reason this still exists is to compare if it is faster or slower
    than AvgRGBMem'''
    
    # ------ initialization method/s ------

    def __init__(self, path, logger = ""):
        # define main path
        self.path = path
        
        # folder environment
        self.avgpath = ""
        self.subfolders = {}
        
        # theres an uncatched error...
        try:
            self.makeavgdir()
        except FileNotFoundError as e:
            print("Folder not found")
        except:
            print("WTF")        

        # create log file in the avg folder
        if logger == "":
            # create a temporary log that only prints to console
            self.mylog = Logger("Avgrgb")
        elif isinstance(logger, Logger):
            # inheriths the logger from somewhere else
            self.mylog = logger
        elif isfile(logger):
            self.mylog = Logger("Avgrgb", logger)
        elif logger == "auto file":
            self.mylog = Logger("Avgrgb", pathfile = join(self.avgpath + "myavglogger.txt"))
        
        
        self.imgs = []
        self.avg = MyRGBImg()
        self.algs = []
        self.algimgs = []
       
    
    def gather_pictures(self):
        ''' The methos checks inside self.path and gather image file'''
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
                mylog.log("Image: {0} imported successfully".format(name + ext))
        
        mylog.log("Successully imported {0} images".format(self.imgs.n))
        

    def average(self, aligned = True):
        ''' averaging procedure, this function saves the newly calculated average'''
        
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
        
        subfolders = ["aligned_rgb_images", "results", "avg_transition"]
        for folder in subfolders:
            self.subfolders[folder] = join(self.avgpath, folder)
            if not isdir(self.subfolders[folder]):
                mkdir(self.subfolders[folder])    


class AvgRGBMemSave(object):
    ''' class to manage the colored average'''
    
    # ------ initialize method ------
    def __init__(self, path, logger = ""):
        # define main path
        self.path = path
        
        # folder environment
        self.avgpath = ""
        self.subfolders = {}
        
        # creates the necessary subfolders
        try:
            self.makeavgdir()
        except FileNotFoundError as e:
            print("Folder not found")
        except:
            print("WTF")        

        # create log file in the avg folder
        if logger == "":
            # create a temporary log that only prints to console
            self.mylog = Logger("Avgrgb")
        elif isinstance(logger, Logger):
            # inheriths the logger from somewhere else
            self.mylog = logger
        elif isfile(logger):
            self.mylog = Logger("Avgrgb", logger)
        elif logger == "auto file":
            self.mylog = Logger("Avgrgb", pathfile = join(self.avgpath + "myavglogger.txt"))
        
        
        # instead of loading all the pictures in one array
        # create a path array that reads the pictures at will
        
        self.imgs_names = []
        self.avg = MyRGBImg()
        self.algs = []
        
        # TODO:
            # transform the getter setters into iterators
        
    
    def get_image(self, index):
        ''' returns a MyRGBImg given the index, loads the original images'''
        # read the image corresponding to the path
        pathtopic = join(self.path, self.imgs_names[index])
        myimg = MyRGBImg()
        myimg.read_from_file(pathtopic)
        return myimg
    
    def get_alg_image(self, index):
        ''' returns a MyRGBImg given the index, loads the aligned images'''
        filename, ext = splitext(self.imgs_names[index])
        pathtopic = join(self.subfolders["aligned_rgb_images"], ("alg_" + filename + ".png" ))
        myimg = MyRGBImg()
        myimg.read_from_file(pathtopic)
        return myimg       
    
    def save_alg_image(self, index, algimg):
        ''' Saves a MyRGBImg given the index, into the alg folder'''
        filename, ext = splitext(self.imgs_names[index])
        # do I have to normalize?
        if not np.all(algimg.data <= 1) or not np.all(algimg.data >= 0):
            algimg.limit(1.0)
        algimg.save(join(self.subfolders["aligned_rgb_images"], ("alg_" + filename + ".png" )))        
    
    def gather_pictures_names(self):
        '''Checks the folder self.path for images and constructs the array
        self.imgs_names which is used to gather the pictures
        '''
        p = self.path
        # gather all the files
        filenames = [f for f in listdir(p) if isfile(join(p, f))]
        for filename in filenames:
            path, name, ext = get_pathname(filename)
            # select only the pictures
            if ext in ['.png', '.jpg']:       
                self.imgs_names.append(filename)
        self.mylog.log("Loaded {0} images.".format(len(self.imgs_names)))
    
    def average(self, mode = "Mode",  aligned = True, debug = False, transition = True):
        if mode == "Mean":
            self.average_mean(aligned, debug, transition)
        if mode == "Median":
            self.average_median(aligned, debug, transition)
        if mode == "Mode":
            self.average_mode(aligned, debug, transition)
        if mode == "Sum":
            self.average_sum(aligned, debug, transition)
    
    def average_mode(self, aligned = True, debug = False, transition = True):
        ''' Calculates the mode of the image array. The mode should represent
        the most frequent pixel value in an image array.
        For size reasons the array is split in quadrants.
        '''
        
        # define the function to get the images according to the alignment
        sizedataset = len(self.imgs_names)
        if aligned:
            get_img = lambda i: self.get_alg_image(i) #self.get_alg_image(0)
        else:
            get_img = lambda i: self.get_image(i) #self.get_image(0)

        # get the image size
        dimx = get_img(0).data.shape[0]
        dimy = get_img(0).data.shape[1]
        
        # get image half size
        dimx2 = int(dimx / 2)
        dimy2 = int(dimy / 2)
        
        # quadrants coordinates as array indices
        quadrant = [(0, dimx2, 0, dimy2) , (dimx2, dimx, 0, dimy2),
                    (0, dimx2, dimy2, dimy), (dimx2, dimx, dimy2, dimy)]
        
        # decide how deep should be the the measured frequency
        # 128 = 8 mil colors
        # True color 24 bbp = 256 = 16'777'260 colors
        depth = 128
        darray = np.arange(depth)
        
        resq = []
        for q in quadrant:
            # calculate for each image, inside a quadrant the mode
            # x, y, c, freq
            stack = np.zeros((dimx2, dimy2, 3, depth), dtype = np.uint32)
            for i in range(sizedataset):
                pic = get_img(i)
                # for each pixel of the image i
                for x, ix in zip(range(q[0], q[1]),range(0, dimx2)):
                    for y, iy in zip(range(q[2], q[3]), range(0, dimy2)):
                        for c in range(3):
                            # test in which bin the pixel goes
                            # len(darray) = depth
                            # the sistem could work with a dictionary too
                            # stack[ix, iy, ic][d] += value
                            # key error -> add the vaule
                            # it should spare memory and computation
                            for d in range(len(darray) - 1):
                                if pic.data[x,y,c] < 0 or pic.data[x,y,c] > 1:
                                    raise ValueError("image not normalized")                                
                                pv = pic.data[x,y,c] * depth
                                if pv >= darray[d] and pv < darray[d + 1]:
                                 stack[ix, iy, c, d] += 1
                                 
            # construct the resulting quadrant and store it in the resq list
            resquadrant = np.zeros((dimx2, dimx2, 3))            
            for x in range(0, dimx2):
                for y in range(0, dimy2):
                    for c in range(0, 3):
                        # for each pixel of quadrant calculate which pixel is 
                        # the most frequent
                        maxfreq = 0
                        maxvalue = 0
                        for i in range(depth):
                            if stack[x, y, c, i] > maxfreq:
                                maxfreq = stack[x, y, c, i]
                                
                                maxvalue = darray[i] / float(depth)
                        resquadrant[x, y, c] = maxvalue
            # this are the averaged quadrants
            calcquadrant = MyRGBImg(resquadrant) 
            resq.append(calcquadrant)
        
        # recompose the picture
        picdata = MyRGBImg(np.zeros((dimx, dimy, 3)))
        for i, q in enumerate(quadrant):
            for x, ix in zip(range(q[0], q[1]), range(quadrant[0][0], quadrant[0][1])):
                for y, iy in zip(range(q[2], q[3]), range(quadrant[0][2], quadrant[0][3])):
                    for c in range(3):
                        picdata.data[x, y, c] = resq[i].data[ix, iy, c]
        self.avg = picdata
        
        if debug:                
            picdata.show_image()
            plt.show()
    
    def average_median(self, aligned = True, debug = False, transition = True):
        ''' Calculats the mean of a serie of pictures aligned takes the 
        pictures from the the rgb aligned folder, while if False takes the 
        original images
        '''
        self.mylog.log("started the median procedure")
        
        # Chose which serie to average
        sizedataset = len(self.imgs_names)
        if aligned:
            get_img = lambda i: self.get_alg_image(i) #self.get_alg_image(0)
        else:
            get_img = lambda i: self.get_image(i) #self.get_image(0)
        
        # get image sizes
        dimx = get_img(0).data.shape[0]
        dimy = get_img(0).data.shape[1]
        dimx2 = int(dimx / 2)
        dimy2 = int(dimy / 2)
        
        # get the quadrant coordinates
        quadrant = [(0, dimx2, 0, dimy2) , (dimx2, dimx, 0, dimy2),
                    (0, dimx2, dimy2, dimy), (dimx2, dimx, dimy2, dimy)]
        
        # construct the median
        resq = []
        for q in quadrant:
            # for each quadrant
            stack = np.zeros((dimx2, dimy2, 3, sizedataset))
            for i in range(sizedataset):
                self.mylog.log("quadrant {0} image {1}".format(q, i))
                pic = get_img(i)
                pic.data = pic.data[q[0]: q[1], q[2] : q[3], :]
                stack[:, :, :, i] = pic.data
            # calculate median
            med = np.median(stack, axis = 3)
            medpic = MyRGBImg(med)
            medpic.show_image()
            plt.show()
            resq.append(medpic)
        
        # recompose the picture
        picdata = MyRGBImg(np.zeros((dimx, dimy, 3)))
        for i, q in enumerate(quadrant):
            for x, ix in zip(range(q[0], q[1]), range(quadrant[0][0], quadrant[0][1])):
                for y, iy in zip(range(q[2], q[3]), range(quadrant[0][2], quadrant[0][3])):
                    for c in range(3):
                        picdata.data[x, y, c] = resq[i].data[ix, iy, c]
        
        # show resulting image
        if debug:
            picdata.show_image()
            plt.show()
        
        self.avg = picdata

    def average_mean(self, aligned = True, debug = False, transition = True):
        ''' performs the mean of the images, aligned is True will use the
        aligned pictures while if false will use the original picture, 
        for the transition, each averaging step is printed out
        '''
        
        self.mylog.log("started the mean averaging procedure")
        
        sizedataset = len(self.imgs_names)
        
        if aligned:
            picture = self.get_alg_image(0)
        else:
            picture = self.get_image(0)       
        
        # initialize sum variable
        s = MyRGBImg(np.zeros(picture.data.shape))
        s = color.rgb2lab(s.data)
        
        for i in range(sizedataset):
            if debug:
                self.mylog.log("Averaging image: " + str(i))
            #load the picture
            if aligned:
                picture = self.get_alg_image(i)
            else:
                picture = self.get_image(i)
            # convert both to lab
            im = color.rgb2lab(picture.data)
            
            #perform operations
            s += im
            
            # if the transition is true show what happens to each picture
            if transition:
                tr = s / float(i + 1)
                avg = MyRGBImg(color.lab2rgb(tr))
                avg.save(join(self.subfolders["avg_transition"], "avg_tr_" + str(i) + ".png"))
                
        # calculate the average    
        s = s / float(sizedataset)
        self.avg = MyRGBImg(color.lab2rgb(s))
        
        # small trick to align the image in the correct sense if they are 
        # squared
        if self.avg.data.shape[0] == self.avg.data.shape[1]:
            self.avg.rotate(90)
            self.avg.flip_V()
    
    def average_sum(self, aligned = True, debug = False, transition = True):
        if aligned:
            get_img = lambda i: self.get_alg_image(i) #self.get_alg_image(0)
        else:
            get_img = lambda i: self.get_image(i) #self.get_image(0)
        
        sizedataset = len(self.imgs_names)
        s = MyRGBImg(np.zeros(get_img(0).data.shape))
        for i in range(sizedataset):
            if debug:
                self.mylog.log("Averaging image: " + str(i))
            #load the picture
            picture = get_img(i)
            
            #perform operations
            s += picture
                            
        # calculate the average    
        self.avg = s
        self.avg.limit(1)        
        
       
    def load_algs(self):
        ''' This function loads the alignments calculated by the avg class'''
        with open(join(self.subfolders["results"], "shifts_log.txt")) as f:
            lines = f.readlines()
        
        self.algs = []
        for line in lines:
            sdata = line.split(' | ')
            sdata = [d.strip() for d in sdata]
            data = [int(sdata[0]), int(sdata[1]), float(sdata[2])]
            self.algs.append(data)
        

        
    def align_images(self, debug = False):
        ''' this function, given the shifts calculated by avg folder class and
        loaded with the self.load_algs method, aligns the original images
        '''
        self.mylog.log("Align procedure started")
        
        self.algimgs = []
        for i in range(len(self.imgs_names)):
            if debug:
                self.mylog.log("Aligning image:" + str(i))
            
            # load picture to align
            algimage = self.get_image(i)
            
            if algimage.data.shape[0] == algimage.data.shape[1]:
                # operations needed to align the rgb images
                algimage.rotate(90)
                algimage.flip_V()            
                algimage.rotate(self.algs[i][2])
                algimage.move(-self.algs[i][0], -self.algs[i][1])
            else:
                # still doesnt work...
                algimage.squareit()
                algimage.rotate(self.algs[i][2])
                algimage.move(-self.algs[i][0], -self.algs[i][1])                

            # save the image
            self.save_alg_image(i, algimage)


    def save_avg(self, name = "avg_rgb.png"):
        ''' saves the average '''
        self.avg.save(join(self.subfolders["results"], name))
            
    def makeavgdir(self):
        ''' create a folder average into the dataset path
         avg
          |- processed_images
          |- aligned_images
          |- correlation_images
          |- results
          |- aligned_rgb_images
          |- avg_transition
        '''
        self.avgpath = join(self.path, "avg")
        if not isdir(self.avgpath):
            mkdir(self.avgpath)
        
        subfolders = ["aligned_rgb_images", "results", "avg_transition"]
        for folder in subfolders:
            self.subfolders[folder] = join(self.avgpath, folder)
            if not isdir(self.subfolders[folder]):
                mkdir(self.subfolders[folder])

    def transpose(self):
        ''' transpose all images '''
        for i, img in enumerate(self.imgs):
            img.transpose()
            self.imgs.set_image(i,img)
        self.mylog.log("images transposed")

    def normalize(self):
        ''' normalize all images '''
        for i, img in enumerate(self.imgs):
            img.normalize()
            self.imgs.set_image(i,img)
        self.mylog.log("images normalized")
    
    def binning(self, n = 1):
        ''' bins all images '''
        for i, img in enumerate(self.imgs):
            img.binning(n)
            self.imgs.set_image(i,img)
        self.mylog.log("images binned")

        
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

    pathtodataset = "../../../silentcam/dataset40/"

    from LogTimes import TimingsTot
    
    t = TimingsTot(pathtodataset + "rgb_time_logfile.log")
    
    avg = AvgRGBMemSave(pathtodataset)
    
    avg.gather_pictures_names()
    t.log("Loaded names")
    
    avg.load_algs()
    t.log("Loaded aligments")
    
    avg.align_images(debug = True)
    t.log("Aligned Images")
    
    avg.average(mode = "Mean", aligned = True, debug = True)
    t.log("Averaged Images")
    
    avg.save_avg()
    
    import winsound
    Freq = 2500 # Set Frequency To 2500 Hertz
    Dur = 1000 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)
