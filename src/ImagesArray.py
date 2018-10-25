# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 22:06:44 2018

@author: Mauro
"""
import os

import my_utils
import Image


class ImagesArray:
    
    def __init__(self, folder):
        self.folder = folder
        self.paths = []
        self.generate_paths(self.folder)
        self.i = 0
        self.n = len(self.paths)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.n:
            img = self.get_image(self.i)
            self.i += 1
            return img
        else:
            self.i = 0
            raise StopIteration()  
    
    def __getitem__(self, i):
        return self.get_image(i)        
    
        
    def generate_paths(self, path):
        # gather files in folder
        names = [my_utils.get_pathname(os.path.join(path, f)) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))] 
        
        self.paths = []
        for n in names:
            if n[2] in ['.jpg', '.png']:
                self.paths.append(os.path.join(n[0], n[1] + n[2]))

    def get_image(self, i):
        path = self.paths[i]
        image = Image.Image(path)
        return image