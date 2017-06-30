# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 05:18:24 2017

@author: Mauro
"""


# This module deals with the Average

# Define Imports

# pyplot
from matplotlib import pyplot as plt

# numpy import

# py imports

# My imports
from AvgFolder_class import AvgFolderMem

# Flat Field correction manager

if __name__ == "__main__":
    
    # gather dark field
    
    pathdfh = "../../../darkfield/horizontal/"
    # average pictures
    
    dfh = AvgFolderMem(pathdfh)
    dfh.gather_pictures()
    dfh.c2gscale()
    dfh.squareit()
    dfh.binning(2)
    
    dfh.average(aligned = False, debug = True)
    
    dfh.save_avg()
    
    dfh.avg.show_image()
    plt.show()
    
    
    pathtodataset = "../../../silentcam/dataset36/"
    
    avg = AvgFolderMem(pathtodataset)
    avg.gather_pictures()
    avg.c2gscale()
    avg.squareit()
    avg.binning(2)
     
    avg.average(aligned = False, debug = True)
    avg.save_avg()
    
    avg.avg.show_image()
    plt.show()