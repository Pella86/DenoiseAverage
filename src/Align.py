# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 22:47:49 2018

@author: Mauro
"""

import os

import ImagesArray
import FFT
import my_utils
import Logging

log = Logging.get_logger(__name__, "DEBUG")

class Align:
    
    def __init__(self, input_dir, output_dir, template):
        self.input_dir = input_dir
        self.aligned_folder = output_dir
        self.template = template
        
        if not os.path.isdir(self.aligned_folder):
            os.mkdir(self.aligned_folder)
    
    def do_alignment(self):
        translationsx = []
        translationsy = []
        
        log.debug("Start alignment")
        imgs = ImagesArray.ImagesArray(self.input_dir)
        for image in imgs:
            image.convert_to_bw()
            image.normalize()
            image_ft = FFT.FFT(image)
            
            c = self.template.template_ft.correlate(image_ft)
            
            peak = c.find_peak()
            log.debug("peak: {}".format(peak))
            dx, dy = c.find_translation(peak)
            
            translationsx.append(dx)
            translationsy.append(dy)
            
            image.move(dx, dy)

            _, name, ext = my_utils.get_pathname(image.filename)
            log.debug("Processed image {}".format(name + ext))
            aligned_img_filename = os.path.join(self.aligned_folder, name + ext)
            image.save_image(aligned_img_filename)    
        
        return (translationsx, translationsy)
        
        
        
        
        
#        files = os.listdir(p.preproc_folder)
#        
#        
#        for file in files[:20]:
#            _, _, ext = my_utils.get_pathname(file)
#            if ext in [".jpg", ".png"]:
#                print(file)
#                img_filename = os.path.join(p.preproc_folder, file)
#                image = Image.Image(img_filename)
#                image.convert_to_bw()
#                image.normalize()
#                image_ft = FFT.FFT(image)
#                
#                c = t.template_ft.correlate(image_ft)
#                
#                peak = c.find_peak()
#                print("peak: ", peak)
#                dx, dy = c.find_translation(peak)
#                
#                translationsx.append(dx)
#                translationsy.append(dy)
#                
#                image.move(dx, dy)
#                
#                aligned_img_filename = os.path.join(aligned_folder, file)
#                image.save_image(aligned_img_filename)