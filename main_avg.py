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
    
<<<<<<< HEAD
<<<<<<< HEAD
    pathtodataset = "../../silentcam/dataset32/"    

    # matplotlib imports
    import matplotlib.pyplot as plt
    
    # My imports
    from AvgFolder_class import AvgFolder

    

    avg = AvgFolder(pathtodataset)
    avg.gather_pictures()
    avg.c2gscale()
    avg.squareit()
    avg.binning(0)    
    avg.transpose()
    avg.normalize() 
    
    avg.save_imgs()

        
    avg.generate_template("UseFirstImage")
    avg.save_template()
    
    avg.template.show_image()
    plt.show()  
    
    avg.template.inspect()
    
    correlate = True
    if correlate:
        # aling dataset
        avg.align_images()
        avg.save_algimgs()
        avg.save_corrs()
        avg.save_shifts()
        
        avg.average()
        avg.save_avg()
        avg.avg.show_image()
        plt.show()

=======
    pathtodataset = "../../silentcam/dataset30/"    
#
#    # matplotlib imports
#    import matplotlib.pyplot as plt
#    
#    # My imports
#    from AvgFolder_class import AvgFolder
#
#    
#
#    avg = AvgFolder(pathtodataset)
#    avg.gather_pictures()
#    avg.c2gscale()
#    avg.squareit()
#    avg.binning(0)    
#    avg.transpose()
#    avg.normalize() 
#    
#    avg.save_imgs()
#
#        
#    avg.generate_template("UseFirstImage")
#    avg.save_template()
#    
#    avg.template.show_image()
#    plt.show()  
#    
#    avg.template.inspect()
#    
#    correlate = True
#    if correlate:
#        # aling dataset
#        avg.align_images()
#        avg.save_algimgs()
#        avg.save_corrs()
#        avg.save_shifts()
#        
#        avg.average()
#        avg.save_avg()
#        avg.avg.show_image()
#        plt.show()
#
>>>>>>> CrossCorrGUI
    from AvgRGB_class import AvgRGB
=======
    import time
>>>>>>> CrossCorrGUI
    
    timenow = time.process_time()
    
    avg = AvgRGB(pathtodataset)
    avg.gather_pictures()
    avg.load_algs()
    avg.align_images()
    avg.average()
    avg.save_avg()
    
    import winsound
    Freq = 2500 # Set Frequency To 2500 Hertz
    Dur = 1000 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)
