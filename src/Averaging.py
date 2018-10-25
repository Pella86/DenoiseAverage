# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 07:42:07 2018

@author: Mauro
"""

import os

import ImagesArray
import Image
import Logging

log = Logging.get_logger(__name__, "DEBUG")

class Average:
    
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.avg_folder = os.path.join(base_dir, "avg")
        if not os.path.isdir(self.avg_folder):
            os.mkdir(self.avg_folder)
    
    def do_average(self, aligned_dir):
        
        imgs = ImagesArray.ImagesArray(aligned_dir)
        
        avg = Image.Image(imgs[0].get_size())
        
        n = 0
        for img in imgs:
            log.debug("Processing image: {}".format(n))
            img.convert_to_bw()
            avg = avg + img
            n += 1   
        avg.save_image(os.path.join(self.avg_folder, "avg.png"))
        
