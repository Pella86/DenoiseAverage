# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:30:42 2017

@author: Mauro

"""

# Define Imports

import sys
sys.path.append("./src")


if __name__ == "__main__":
    print("START AVERAGING SCRIPT")
    
    import time
    
    timenow = time.process_time()
    
    pathtodataset = "../../silentcam/dataset35/"  
    
    avgtype = "gray"
    sound = False
    
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
            s  = "Elapsed time for subprocess:{0}\n".format(subtime)
            
            totaltime = self.nowtime - self.starttime
            totaltime = self.convert_in_ddhhss(totaltime)
            s += "Time total elapsed: {0}".format(totaltime)
            
            self.lastcall = time.process_time()
            return s
    
    t = Timings() 

    
    if avgtype == "gray":
    
        # matplotlib imports
        import matplotlib.pyplot as plt
        
        # My imports
        from AvgFolder_class import AvgFolder
    
        
    
        avg = AvgFolder(pathtodataset)
        print("gathering pictures...")
        avg.gather_pictures()
        print(t)
        
        print("Gray scale")
        avg.c2gscale()
        print(t)
        print("Square pictures")
        avg.squareit()
        print(t)
        print("Binning")
        avg.binning(0)   
        print(t)
        print("Transpose")
        avg.transpose()
        print(t)
        print("Normalize")
        avg.normalize() 
        print(t)
        
        print("Save alg images...")
        avg.save_imgs()
        print(t)
    
        print("Generate Template...")    
        avg.generate_template("UseFirstImage")
        avg.save_template()
        
        avg.template.show_image()
        plt.show()  
        
        avg.template.inspect()
        print(t)
        
        correlate = True
        if correlate:
            # aling dataset
            print("Align images...")
            avg.align_images(True)
            print(t)
            
            print("Save images...")
            avg.save_algimgs()
            avg.save_corrs()
            avg.save_shifts()
            print(t)
            
            print("Average images...")
            avg.average()
            avg.save_avg()
            avg.avg.show_image()
            plt.show()
            print(t)

    if avgtype == "rgb":
        from AvgRGB_class import AvgRGB
        
        
        avg = AvgRGB(pathtodataset)
        
        print("Gathering pictures...")
        avg.gather_pictures()
        print(t)
        
        print("Loading algs...")
        avg.load_algs()
        print(t)
        
        print("Align pictures...")
        avg.align_images()
        print(t)
        
        print("Average pictures...")
        avg.average()
        print(t)
        
        avg.save_avg()
    
    if sound:
        import winsound
        Freq = 2500 # Set Frequency To 2500 Hertz
        Dur = 1000 # Set Duration To 1000 ms == 1 second
        winsound.Beep(Freq,Dur)
    
    print("SCRIPT FINISH!")
