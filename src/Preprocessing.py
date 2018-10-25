# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 18:44:28 2018

@author: Mauro
"""

# preprocessing takes a config file with the operations written
# executes in batch for every image in the folder
# writes to file preprocessing: successful

import os

import Image
import Logging
import my_utils
import ImagesArray

log = Logging.get_logger(__name__, "DEBUG")

test_dataset = r"C:\Users\Mauro\Desktop\Vita Online\Programming\Picture cross corr\samsung_S8\dataset_1"
    


class Preprocess:
    
    def __init__(self, base_dir):
        
        self.base_dir = base_dir
        self.preproc_folder = os.path.join(self.base_dir, "preprocessed")
    
    def init_processing(self):
        
        # create the preprocessing folder
        if not os.path.isdir(self.preproc_folder):
            os.mkdir(self.preproc_folder)
        
        # read the config file
        config_filename = os.path.join(self.base_dir, "config_preprocess.txt")
        with open(config_filename, "r") as f:
            lines = f.readlines()

        # creates the operation list
        # oplist = [[func, args], ...]
        log.debug("Parsing config file...")
        oplist = []
        for line in lines:
            op = line.split(" ")

            op = [o.strip() for o in op]
            
            # if the function has arguments
            if len(op) > 1:
                tmp_op = [op[0]]
                # transform each argument according to the prefix
                for arg in (op[1:]):
                    if arg[0] == "i":
                        parg = int(arg[1:])
                        tmp_op.append(parg)
                op = tmp_op

            oplist.append(op)
        
        log.debug("Operations retrived")
        for op in oplist:
            log.debug(" ".join(str(f) for f in op))
            
        log.debug("Begin Processing")
        imgs = ImagesArray.ImagesArray(self.base_dir)
        for img in imgs:
            # applies the operation list
            for op in oplist:
                method = getattr(img, op[0])
                
                # if the function has argument
                if len(op) >= 2:
                    method(*op[1:])
                else:
                    method()
            
            img.limit(1)
            
            log.debug("processed: " + img.filename)
            _, name, _ = my_utils.get_pathname(img.filename)
            save_name = os.path.join(self.preproc_folder, name + ".png")
            img.save_image(save_name)            

#   


if __name__ == "__main__":
    p = Preprocess(test_dataset)