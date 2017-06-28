# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 07:06:41 2017

@author: Mauro
"""

# impoorts

# py imports

import time

# Timing utils

class TimingsTot:
    def __init__(self, path = None, debug_mode = True):
        self.starttime = time.perf_counter()
        self.nowtime = time.perf_counter()
        self.lastcall = time.perf_counter()
        
        self.logfilepath = path
        self.debug_mode = debug_mode
    
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
    
    def logtimestr(self, title):
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