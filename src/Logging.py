# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 23:36:58 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================
import logging
import datetime

#==============================================================================
# Constants
#==============================================================================

debug_level_logging = {}
debug_level_logging["NOTSET"] = logging.NOTSET
debug_level_logging["DEBUG"] = logging.DEBUG
debug_level_logging["INFO"] = logging.INFO
debug_level_logging["WARNING"] = logging.WARNING
debug_level_logging["ERROR"] = logging.ERROR
debug_level_logging["CRITICAL"] = logging.CRITICAL

#==============================================================================
# function
#==============================================================================

def get_logger(name, debug_level):

    log = logging.getLogger(name)
    
    # set logger level
    log.setLevel(debug_level_logging[debug_level])
    
    # create a file handler
    fh = logging.FileHandler("log_" + datetime.datetime.now().strftime("%y%m%d") + ".log")
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    # create console and file handler
    log.addHandler(fh)
    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s - %(message)s')
    sh.setFormatter(formatter)
    log.addHandler(sh)
    
    return log