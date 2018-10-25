# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 20:32:50 2018

@author: Mauro
"""

import os
import my_utils
import Image
import FFT
import ImagesArray

class Template:
    
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.template_dir = os.path.join(base_dir, "template_dir")
        self.template = None
        self.template_ft = None

        if not os.path.isdir(self.template_dir):
            os.mkdir(self.template_dir)
        
    def pick_first_image(self, folder):
        # take first preprocessing image
        imgs = ImagesArray.ImagesArray(folder)
        self.template = imgs[0]
        self.template.convert_to_bw()
        self.template.normalize()       
#        files = os.listdir(folder)
#        for file in files:
#            _,name, ext = my_utils.get_pathname(file)
#            if ext in [".jpg", ".png"]:
#                self.template = Image.Image(os.path.join(folder, file))
#                self.template.convert_to_bw()
#                self.template.normalize()
#                break
    
    def calc_ft(self):
        if self.template is None: raise Exception("Uninitialized template")
        self.template_ft = FFT.FFT(self.template)
    