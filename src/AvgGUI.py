# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 19:04:02 2017

@author: Mauro
"""

# TkInter
from tkinter import (Tk, Frame, Text, Label, Canvas, PhotoImage, StringVar,
                     Button)

# py imports
from os import mkdir 
from os.path import join, isdir, split, splitext
from copy import deepcopy

# matlibplot imports
from scipy.misc import imsave

# My imports
from AvgFolder_class import AvgFolderMem
from MyImage_class import MyImage
from MyRGBImage_class import MyRGBImg
from ImageFFT_class import ImgFFT

# numpy import
import numpy as np



#from matplotlib import pyplot as plt


def get_pathname(path):
    ''' Little function to split the path in path, name, extension'''
    path, nameext = split(path)
    name, ext = splitext(nameext)
    return path, name, ext

class ConnectIndex:
    
    def __init__(self, i):
        self.idx = i
    
    def get(self):
        print(self.idx)
        return self.idx
    
    def __add__(self, rhs):
        return ConnectIndex(self.idx + rhs)
    
    def __sub__(self, rhs):
        return ConnectIndex(self.idx - rhs)
    
    def __str__(self):
        return str(self.idx)
    
    def __lt__(self, rhs):
        if type(rhs) == int:
            crhs = ConnectIndex(rhs)
        else:
            crhs = rhs
        if self.idx < crhs.idx:
            return True
        else:
            return False

    def __gt__(self, rhs):
        if type(rhs) == int:
            crhs = ConnectIndex(rhs)
        else:
            crhs = rhs
        if self.idx > crhs.idx:
            return True
        else:
            return False
    
    def __cmp__(self, rhs):
        if self.idx <  rhs.idx:
            return -1
        if self.idx == rhs.idx:
            return 0
        if self.idx > rhs.idx:
            return 1

class LifoStack:
    
    def __init__(self, sizestack = 0, widthstack = 0):
        self.sizestack = sizestack
        self.widthstack = widthstack
        self.stack = []
        self.i = 0
        
    def add(self, element):
        element = element[:self.widthstack]
        if len(self.stack) < self.sizestack:
            self.stack.append(element)
        else:
            self.stack.pop(0)
            self.stack.append(element)
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.i < len(self.stack):
            text = self.stack[self.i]
            self.i += 1
            return text
        else:
            self.i = 0
            raise StopIteration()  

class ConsWidget:
    
    def __init__(self, frame):
        self.h = 40 
        self.w = 40
        self.textbox = Text(frame, height = self.h, width = self.w)
        
        self.textstack = LifoStack(self.h, self.w)
    
    def add_text(self, text):
        self.textstack.add(text)
        # create the text
        s = ""
        for line in self.textstack:
           s += line + '\n'
        s = s[:-1]
           
        self.textbox.delete("1.0","end")
        self.textbox.insert('1.0', s)
    
        
    
    def get_coords_txt(self, x, y):
        return "[0:d].[1:d]".format()

class ImagesManager:
    
    def __init__(self, avg, csize):
        
        self.avg = avg
        self.csize = csize
        
        # create the temp folder
        self.tmppath = join(self.avg.avgpath, "tmp_gui_img")
        if not isdir(self.tmppath):
            mkdir(self.tmppath)    
        
        self.refdb = {}
    
    def get_image(self, inpath):
        print("ImagesManager.get_image()")
        print(inpath)
        try:
            mygifpath = self.refdb[inpath]
        except KeyError:
            # create the ref image
            path, name, ext = get_pathname(inpath)
            mygifpath = join(self.tmppath, name + '.gif')
            self.savegif(inpath, mygifpath, (self.csize[0], self.csize[1]))
            self.refdb[path] = mygifpath
        return mygifpath
        

    def savegif(self, path, gifpath, size):
        image = MyImage(path)
        image.convert2grayscale()
        image.squareit()
        
        # calculate ft for resizing
        imft = ImgFFT(image.data)
        imft.ft()
        im = imft.resize_image(size[0], size[1])
        
        imrgb = MyRGBImg(np.zeros((size[0], size[1], 3)))
        for c in range(3):
            imrgb.set_channel(im, c)
        
        
        # save resized image
        imsave(gifpath, imrgb.data, format = "gif")


class ImageCanv:

    def __init__(self, frame, title, size, avg, outputc):
        self.outputc = outputc


        
        self.cframe = Frame(frame)
        self.cframe.image = {}
        
        # add title
        titlel = Label(self.cframe, text = title)
        titlel.grid(row = 0, column = 0)
        
        # define the canvas display
        cw = size[0]
        ch = size[1]
        
        self.canvas = Canvas(self.cframe, width=ch, height=cw)
        self.canvas.grid(row = 1, column = 0)  
        
        # use the image manager to create the path needed to work
        self.imgman = ImagesManager(avg, (ch, cw))
    
    def show_image(self, path):
        ''' display the image in the canvas'''
        gifpath = self.imgman.get_image(path)
        inimage = PhotoImage(file = gifpath)
        # get a unique id
        name = get_pathname(gifpath)
        self.outputc.add_text("Loading image... " + name[1] + name[2])
        self.cframe.image[name[1]] = inimage
        self.canvas.create_image(0, 0 , image = inimage, anchor = "nw")

class ImageCanvSeq(ImageCanv):
    
    def __init__(self, frame, imgseq, title, size, avg, outputc):        
        self.frame = Frame(frame)
        super(ImageCanvSeq, self).__init__(self.frame, title, size, avg, outputc)
        
        
        self.imgseq = imgseq
        self.maximgs = ConnectIndex(self.imgseq.n)
        self.idx = None
        

        
        # add the left button
        self.prev = Button(self.frame, text = "<", command = self.prev_pic )
        self.prev.grid(row = 0, column = 0)
 
        # add cunter string
        self.counterstr = StringVar()
        self.counterstr.set("default")
        
        
        l = Label(self.frame, textvariable = self.counterstr)
        l.grid(row = 0, column = 1)  
       
        # add the left button
        self.prev = Button(self.frame, text = ">", command = self.next_pic )
        self.prev.grid(row = 0, column = 2)  
        
        # add the canvas
        self.cframe.grid(row = 1, column = 0, columnspan = 3)
        


    def update_seq_count(self):
        s = "Image {0}/{1}".format(str(self.idx + 1), str(self.maximgs))
        self.counterstr.set(s)
        
    
    def prev_pic(self):
        if self.idx > 0:
            self.idx -= 1
            self.show_image(self.imgseq.get_path_to_img(self.idx.get()))
            self.update_seq_count()
            
    
    def next_pic(self):
        if self.idx < (self.maximgs - 1):
            self.idx += 1
            self.show_image(self.imgseq.get_path_to_img(self.idx.get()))
            self.update_seq_count()
            
    def update(self, i):
        self.idx = deepcopy(i)
        self.show_image(self.imgseq.get_path_to_img(self.idx.get()))
        self.update_seq_count()
            

        

class AvgMain:
    
    def __init__(self, root, path):
        
        # main path
        self.mpath = path
        
        # create main  frame
        self.mframe = Frame(root)
        self.mframe.image = {}
        
        self.consoleframe = Frame(self.mframe)
        self.consoleframe.grid(row = 0, column = 0, rowspan = 2)
        
        # add a beauty label
        l = Label(self.consoleframe, text = "Console:")
        l.grid(row = 0, column = 0)
        
        # create text box as a console
        self.constext = ConsWidget(self.consoleframe)
        self.constext.textbox.grid(row = 1, column = 0)
        
        # use the averaging class to load the images from the folder
        self.myavg = AvgFolderMem(self.mpath)
        self.myavg.gather_pictures()
        
        self.image_index = ConnectIndex(0)
        self.max_images = self.myavg.init_imgs.n
        
        titles = ["Initial Images", "Processed Images", "Aligned Images", "Corr Images"]
        positions = [(0,1), (0,3), (0,4), (1, 2)]
        myimgseqs = [self.myavg.init_imgs, self.myavg.imgs, self.myavg.algimgs, self.myavg.corrs]
        self.canvarr = []
        
        for title, position, imgseq in zip(titles, positions, myimgseqs):
            frame = Frame(self.mframe)
            frame.grid(row = position[0], column = position[1])
            
            mycanv = ImageCanvSeq(frame, imgseq, title, (256,256), self.myavg, self.constext)
            mycanv.frame.pack()
            
            self.canvarr.append(mycanv)
            
        # create a text box
            
        
        # give a canvas for the averaged image
        self.avgimg = Frame(self.mframe)
        self.avgimg.grid(row = 0, column = 5)
                
        myimg = ImageCanv(self.avgimg, "Average", (256, 256), self.myavg, self.constext)
        myimg.cframe.grid(row = 0, column = 0)  
        
        pathtoavg = self.myavg.get_avg_path()
        myimg.show_image(pathtoavg)  

       
        # give a canvas for the template images
        self.templateimg = Frame(self.mframe)
        self.templateimg.grid(row = 1, column = 1)
                
        myimg = ImageCanv(self.templateimg, "Template", (256, 256), self.myavg, self.constext)
        myimg.cframe.grid(row = 0, column = 0)  
        
        pathtotemplate = self.myavg.get_template_path()
        myimg.show_image(pathtotemplate)      
        
        # add the shift and angles
        
        # buttons to control images together
        
        bleft = Button(self.mframe, text = "< conn", command = self.prev_pic)
        bleft.grid(row = 2, column = 1)

        bright = Button(self.mframe, text = "conn >", command = self.next_pic)
        bright.grid(row = 2, column = 3)  
        
        # create custom cross correlation
        # create a button analyze correlation.
        bcorr = Button(self.mframe, text = "correlate", command = self.correlate)
        bcorr.grid(row = 2, column = 2)
        
        # to do
        # - add the custom cross corr panel
        # - add the shift angle panel
        # - add the calculate option
        # - add the process picture panel

    def prev_pic(self):
        self.image_index -= 1
        for canv in self.canvarr:
            if self.image_index > 0:
                
                canv.update(self.image_index)

    def next_pic(self):
        self.image_index += 1
        for canv in self.canvarr:
            if self.image_index < (self.max_images - 1):
                canv.update(self.image_index)
    
    def correlate(self):
        # get the two images and pass them to Cross corr gui.
        idx = self.image_index
        
        # get the processed image
        procimg = self.imgs[i].get_path
        
        # template
        template = self.myavg.get_path_to_template()
        
        # load the Cross Corr GUI
        # create a widget...
        
      

if __name__ == "__main__":
    
    path = "../../../silentcam/dataset36/"
    
    # initializate Tk root
    root = Tk()   
    
    m = AvgMain(root, path)
    m.mframe.pack()
    
    # start the loop
    root.mainloop()  