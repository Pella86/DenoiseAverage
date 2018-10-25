# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 20:25:49 2018

@author: Mauro
"""

import os

def get_pathname(path):
    ''' Little function to split the path in path, name, extension'''
    path, nameext = os.path.split(path)
    name, ext = os.path.splitext(nameext)
    return path, name, ext