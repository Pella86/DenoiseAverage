# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:30:42 2017

@author: Mauro

"""

# Define Imports

import sys
sys.path.append("./src")


# numpy import
import numpy as np

# matplotlib imports
from matplotlib import pyplot as plt

# pyimpots
from os.path import isdir, isfile, join, splitext, split
from os import listdir, mkdir
from copy import deepcopy

# myimports
from LogTimes import Logger
from AvgFolder_class import AvgFolderMem, AvgFolder
from MyImage_class import MyImage


def run_create_test_dataset():
    debug_mode = True
    
    testdatasetpath = "../../../silentcam/testdataset/"
    mypicname = "../../../Lenna.png"    
    
    mylog = Logger("Create gray dataset", testdatasetpath + "main_logfile.txt", debug_mode = debug_mode)
    
    mylog.log("Creating dataset in:\n" + testdatasetpath)
    mylog.log("Using the picture: " + mypicname)
    
    

    if not isdir(testdatasetpath):
        mkdir(testdatasetpath)  
    
    logpathdir = join(testdatasetpath, "tlog")
    if not isdir(logpathdir):
        mkdir(logpathdir)    
    
    # create a test dataset:

    mypic = MyImage(mypicname)
    mypic.squareit()
    mypic.convert2grayscale()
    mypic.binning(2)
    mypic.normalize()
    
    mylog.log("Processing done")
    
    template_folder = join(testdatasetpath, "template_folder")
    
    if not isdir(template_folder):
        mkdir(template_folder)
        
    mypic.save(join(template_folder, "template.png"))
    mylog.log("Saved the original image in the template folder")
    
    if debug_mode:
        mypic.show_image()
        plt.show()
    
    mylog.log("------------------------------\Creating dataset\n------------------------------")

    np.random.seed(5)

    datasetangles = []
    datasetshifts = []   
    datatrans = []
    

    
    
    with open(join(logpathdir, "mytransformations.log"), 'w') as f:
        for i in range(10):
            image = deepcopy(mypic)
           
            anglefirst = False if np.random.randint(0,2) == 0 else True
            angle = np.random.randint(-10, 10) / float(10)
            dx = np.random.randint(-25, 25)
            dy = np.random.randint(-25, 25)
            
            f.write("{0} {1} {2} {3}\n".format(anglefirst, angle, dx, dy))
            
            
            datatrans.append((anglefirst, angle, dx, dy))
            
            if anglefirst:
                datasetangles.append(angle)
                image.rotate(angle)
    
                datasetshifts.append((dx,dy))
                image.move(dx, dy)
            else:
                datasetshifts.append((dx,dy))
                image.move(dx, dy) 
    
                datasetangles.append(angle)
                image.rotate(angle)
            
            print(datatrans[i])
               
            image.show_image()
            plt.show()
            
            image.save(join(testdatasetpath, "pic_" + str(i) + ".png"))             

def run_average_gray():
       # options  
    debug_mode = True
    
    # chose path to image sequence folder
    datasetpath = "../../silentcam/testdataset/"    
    
    memsave = True # True | False
    
    preprocop = [("convert to grayscale",),
                 ("square it",),
                 ("binning", 0),
                 ("transpose",),
                 ("normalize",)]
    
    custom_template = False # True | False
    template_image_path = None # path to image
    
    auto_template_type = "UseFirstImage" # "Use First Image" | "Average"
    save_template = True # True | False
    
    align_images = True # True | False
    align_mode = "fixed" # "fixed | tree"
    align_space = (-1.2, 1.2, 0.1) # (min angle, max angle, precision)
    
    
    
    
    # logger
    mylog = Logger("Averaging Gray", datasetpath + "main_logfile.txt", debug_mode = debug_mode)

    mylog.log("Debug mode: " + "ON" if debug_mode == True else "OFF")
    mylog.log("For the folder:")
    mylog.log(datasetpath)
    mylog.log("Averaging type: grey")
    mylog.log("Memory saving mode: " + str(memsave))
    
        
        
        
    mylog.log("------------------------------\nLoading dataset\n------------------------------")
    if memsave:
        avg = AvgFolderMem(datasetpath)
    else:
        avg = AvgFolder(datasetpath)
        
    
    avg.gather_pictures()
    # build the informatiosn
    mylog.log("number of pictures:" + str(avg.init_imgs.n))
    image = avg.init_imgs.get_image(0)
    mylog.log("Size of images: " + str(image.data.shape[0]) + "x" + str(image.data.shape[1]))
    
    mylog.log("--- Start preporcessing ---", True)
    
    nametofunc = {} 
    nametofunc[preprocop[0]] = lambda : avg.c2gscale()
    nametofunc[preprocop[1]] = lambda : avg.squareit()
    nametofunc[preprocop[2]] = lambda n : avg.binning(n)
    nametofunc[preprocop[3]] = lambda : avg.transpose()
    nametofunc[preprocop[4]] = lambda : avg.normalize()
    
    for name in preprocop:
        if len(name) == 1:
            nametofunc[name]()
            mylog.log("Process: " + name[0])
        if len(name) == 2:
            nametofunc[name](name[1])
            mylog.log("Process: " + name[0] + "Arguments: " + str(name[1]))
    mylog.log("Processing took: ", True)
    
    mylog.log("------------------------------\nGenerating template\n------------------------------")
    
    if custom_template:
        custom_t = MyImage(template_image_path)
        custom_t.convert2grayscale()
        mylog.log("Template loaded from: " + template_image_path)
        mylog.log("Template image is: " + custom_t.get_sizex() + "x" + custom_t.get_sizey())
        avg.generate_template(custom_t)
    else:
        avg.generate_template(auto_template_type)
        mylog.log("Template generated: " + auto_template_type)
    
    mylog.log("Template generated", True)
    
    if save_template:
        avg.save_template()
    
    if debug_mode:
        avg.template.show_image()
        plt.show()  
        avg.template.inspect()

    
    if align_images:
        mylog.log("------------------------------\nAlignment\n------------------------------")
        mylog.log("Choosen Aligment: " + align_mode)
        alignnames = ["min angle: ", " |max angle: ", " |precision: "]
        mylog.log("".join(a + str(d) for a, d in zip(alignnames, align_space)))
        avg.align_images(align_mode, align_space, debug_mode)
        avg.save_shifts()
        
        mylog.log("Alignment done", True)
        if avg.anglestree != None:
            mylog.log("Numnber of template generated: " + str(len(avg.anglestree.angles_nodes)))
            mylog.log("Normally would be: " + str(len(np.arange(align_space[0], align_space[1], align_space[2]))))
        else:
           mylog.log("Numnber of template generated: " + str(avg.templaterotsft.n)) 
        mylog.log("Shifts saved")
        
        mylog.log("------------------------------\nAverage\n------------------------------")
        avg.average(debug = debug_mode)
        avg.save_avg()
        mylog.log("Average Complete", True)
        
        if debug_mode:
            avg.avg.show_image()
            plt.show() 
            avg.avg.inspect()                
        
    mylog.log("End procedure", True)

if __name__ == "__main__":
    print("START AVERAGING SCRIPT")
    
    run_gavg = True
    if run_gavg:
        run_average_gray()
 
    
    print("SCRIPT FINISH!")
