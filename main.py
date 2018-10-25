# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 08:43:16 2018

@author: Mauro
"""

# append the src folder in the "searched paths"
import sys
sys.path.append("./src")

# imports

from copy import deepcopy
import os

import matplotlib.pyplot as plt
import numpy as np

import Image
import Preprocessing
import Logging
import FFT
import my_utils
import Template
import Align
import ImagesArray
import Averaging
import AlignRot


log = Logging.get_logger(__name__, "DEBUG")
 


# main program
if __name__ == "__main__":
    log.info("Averaging program started") 

    base_dir = r"C:\Users\Mauro\Desktop\Vita Online\Programming\Picture cross corr\samsung_S8\dataset_1"
    
    #base_dir = r"C:\Users\Mauro\Desktop\Vita Online\Programming\Picture cross corr\samsung_S8\test_dataset_new"

    # Preprocess the pictures
    p = Preprocessing.Preprocess(base_dir)
#    p.init_processing()

    # create template
    template = Template.Template(base_dir)
    template.pick_first_image(p.preproc_folder)
    template.calc_ft()
    
    
    # for every image in the preproc folder calculate the correlation
    # then move each image to the right place in the
    # aligned folder
    first_alg_output =  os.path.join(base_dir, "first_alg")
    alg = Align.Align(p.preproc_folder, first_alg_output, template)
#    alg.do_alignment()
    
    # rotation alignment
    
    # create and store the template ft
    rot_alg_dir = os.path.join(base_dir, "rot_aligned")
    rotalg = AlignRot.AlignRot(first_alg_output, rot_alg_dir, template, (-10, 10, 0.4))
    rotalg.create_rotated_templates()
    rotalg.do_alignment()
    
    # redo translation alignment
    second_alg_output =  os.path.join(base_dir, "second_alg")
    alg = Align.Align(rot_alg_dir, second_alg_output, template)
    alg.do_alignment()    
    
    # average images
    avg = Averaging.Average(base_dir)
    avg.do_average(second_alg_output)
    
    
    print("----done---")
    