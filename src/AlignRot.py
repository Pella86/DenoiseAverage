# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:45:16 2018

@author: Mauro
"""

import os
from copy import deepcopy

import numpy as np

import FFT
import Logging
import ImagesArray
import my_utils

log = Logging.get_logger(__name__, "DEBUG")

class AlignRot:
    
    def __init__(self, input_dir, output_dir, template, angle_span):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.template = template
        
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)
        
        # create the template rotations
        self.template_fts = None
        
        # create the angle span
        self.angles = np.arange(*angle_span)
        

    def create_rotated_templates(self):
        self.template_fts = []
        for angle in self.angles:
            tmp_template = deepcopy(self.template.template)
            tmp_template.rotate(angle)
            ft = FFT.FFT(tmp_template)
            self.template_fts.append(ft)
    
    def do_alignment(self):
        imgs = ImagesArray.ImagesArray(self.input_dir)
        for image in imgs:
            log.debug("calculating...")
            image.convert_to_bw()
            image.normalize()
            imageft = FFT.FFT(image)
            smax = 0
            angle = 0
            for angle_idx, tft in enumerate(self.template_fts):
                corr = tft.correlate(imageft)
                s, dx, dy = corr.find_peak()
                if s > smax:
                    angle = self.angles[angle_idx]
                    smax = s
            
            log.debug("Angle found: {}, {:.2}".format(angle, smax))
            
            image.rotate(-angle)
            image.limit(1)
            
            _, name, ext = my_utils.get_pathname(image.filename)
            image_filename = os.path.join(self.output_dir, name + ext)
            image.save_image(image_filename)
    
#    if not os.path.isdir(rot_alg_dir):
#        os.mkdir(rot_alg_dir)
#    
#    angle_span = (-10, 10, 0.4)
#    angles = np.arange(*angle_span)
#    print(len(angles))
#    print(angles)
#    
#    template_fts = []
#    for angle in angles:
#        tmp_template = deepcopy(template.template)
#        tmp_template.rotate(angle)
#        ft = FFT.FFT(tmp_template)
#        template_fts.append(ft)
#    
#    imgs = ImagesArray.ImagesArray(alg.aligned_folder)
#    for image in imgs:
#        print("calculating")
#        image.convert_to_bw()
#        image.normalize()
#        imageft = FFT.FFT(image)
#        smax = 0
#        angle = 0
#        for angle_idx, tft in enumerate(template_fts):
#            corr = tft.correlate(imageft)
#            s, dx, dy = corr.find_peak()
#            if s > smax:
#                angle = angles[angle_idx]
#                smax = s
#        print(angle, smax)
#        
#        image.rotate(-angle)
#        image.limit(1)
#        _, name, ext = my_utils.get_pathname(image.filename)
#        image_filename = os.path.join(rot_alg_dir, name + ext)
#        image.save_image(image_filename)