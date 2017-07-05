# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 07:06:41 2017

@author: Mauro
"""

# impoorts

# py imports

import time
import datetime

# Timing utils

class Logger:
    ''' This class will manage the logging '''
    
    def __init__(self, title = None, pathfile = None, debug_mode = True):
        self.path_file = pathfile
        self.debug_mode = debug_mode
        self.starttime = time.perf_counter()
        self.nowtime = time.perf_counter()
        self.lastcall = time.perf_counter() 
        
        if title is not None:
            today = datetime.datetime.now()   
            s = title + " program started the " + today.strftime("%d of %b %Y at %H:%M")
            self.log("=============================================================\n" +
                     s +
                     "\n=============================================================")           



    def convert_in_ddhhss(self, seconds):
        hh = 0
        mm = 0
        ss = 0
        mm, ss = divmod(int(seconds), 60)
        hh, mm = divmod(mm, 60)    
        
        return "{0:0>2}:{1:0>2}:{2:0>2}".format(hh, mm, ss)
    
    def gettimestr(self):
        self.nowtime = time.perf_counter()
        subtime =  self.nowtime - self.lastcall
        subtime = self.convert_in_ddhhss(subtime)
        s  = "Elapsed time for subprocess: {0}\n".format(subtime)
        
        totaltime = self.nowtime - self.starttime
        totaltime = self.convert_in_ddhhss(totaltime)
        s += "Total elapsed time: {0}".format(totaltime)
        
        self.lastcall = time.perf_counter()
        return s
    
    def log(self, title, time_log = False):
        if time_log:
            s = title + '\n'
            s += self.gettimestr() + '\n'
        else:
            s = title + '\n'
            
        if self.path_file is not None:
            with open(self.path_file, 'a') as f:
                f.write(s)
                
        if self.debug_mode:
            print(s)        

class TimingsTot:
    def __init__(self, path = None, title = "insert date time here", debug_mode = True):
        self.starttime = time.perf_counter()
        self.nowtime = time.perf_counter()
        self.lastcall = time.perf_counter()
        
        self.logfilepath = path
        self.debug_mode = debug_mode
        
        with open(self.logfilepath, 'a') as f:
            f.write("--------"+ title + "---------\n")
    
    def convert_in_ddhhss(self, seconds):
        hh = 0
        mm = 0
        ss = 0
        mm, ss = divmod(int(seconds), 60)
        hh, mm = divmod(mm, 60)    
        
        return "{0:0>2}:{1:0>2}:{2:0>2}".format(hh, mm, ss)
    
    def gettimestr(self):
        self.nowtime = time.perf_counter()
        subtime =  self.nowtime - self.lastcall
        subtime = self.convert_in_ddhhss(subtime)
        s  = "Elapsed time for subprocess: {0}\n".format(subtime)
        
        totaltime = self.nowtime - self.starttime
        totaltime = self.convert_in_ddhhss(totaltime)
        s += "Total elapsed time: {0}".format(totaltime)
        
        self.lastcall = time.perf_counter()
        return s
    
    def log(self, title):
        s = self.gettimestr()
        if self.logfilepath != None:
            with open(self.logfilepath, 'a') as f:
                f.write(title + '\n')
                f.write(s + '\n')
        if self.debug_mode:
            print(title)
            print(s)
    
    def __str__(self):
        s = 'Not available'
        return s    


class Timings:
    def __init__(self):
        self.starttime = time.process_time()
        self.nowtime = time.process_time()
        self.lastcall = time.process_time()
    
    def convert_in_ddhhss(self, seconds):
        hh = 0
        mm = 0
        ss = 0
        mm, ss = divmod(int(seconds), 60)
        hh, mm = divmod(mm, 60)    
        
        return "{0:0>2}:{1:0>2}:{2:0>2}".format(hh, mm, ss)
    
    def __str__(self):
        self.nowtime = time.process_time()
        subtime =  self.nowtime - self.lastcall
        subtime = self.convert_in_ddhhss(subtime)
        s  = "Elapsed time for subprocess: {0}\n".format(subtime)
        
        totaltime = self.nowtime - self.starttime
        totaltime = self.convert_in_ddhhss(totaltime)
        s += "Time total elapsed: {0}".format(totaltime)
        
        self.lastcall = time.process_time()
        return s