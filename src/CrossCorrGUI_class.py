# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:44:04 2017

@author: Mauro

The idea of the script is to create a small GUI managing the bandpass filter.
Since Tkinter can import only GIF image, an interface creates the images and
saves them in  a buffer folder, that are then read by the GUI class
"""

#==============================================================================
# Define Imports
#==============================================================================

# TkInter
from tkinter import (Tk, PhotoImage, Label, Frame, Canvas, Entry, Button, Menu,
                     filedialog, StringVar, IntVar, Checkbutton)

# sys imports
from os import mkdir 
from os.path import join, split, isdir, splitext
from shutil import rmtree
from copy import deepcopy

# matlibplot imports
from scipy.misc import imsave

# my imports
from MyImage_class import MyImage, Mask
from ImageFFT_class import ImgFFT

# todo today:
    # load file button        V
    # save files button:      V
        # save composite      
        # save single images  V
        # save algs           V
    # add loading screen
    # add inspect label       V
    # support for RGB images


#==============================================================================
# Define Class managing image
#==============================================================================

def get_pathname(path):
        path, nameext = split(path)
        name, ext = splitext(nameext)
        return path, name, ext


class ImagePath:

    def __init__(self, name, image, bufpath):
        self.image = image
        self.name = name
        self.gifname = join(bufpath, self.name) + '.gif'

class ImageManager:
    
    def __init__(self, imagepathname):
        
        self.initialpath = imagepathname
        
        path, name, ext = get_pathname(self.initialpath)
        self.mainpath = path
        self.name = name
        self.inimg_name = self.name + ext

        # create the directory for the elaboration
        self.bufpath = join(self.mainpath,self.name)
        if not isdir(self.bufpath):
            mkdir(self.bufpath)

        # open the source image
        self.inimage = ImagePath(self.name, MyImage(), self.bufpath)

        # declare the fourier transform
        self.ftimage = 0
        
        # TODO        
        # findppeak on the better cc
        # represent it with the tkinter canvas

    def init_inimage(self):
        # open the source image
        self.inimage = ImagePath(self.name, MyImage(), self.bufpath)
        self.inimage.image.read_from_file(self.initialpath)
        self.inimage.image.convert2grayscale()
        self.inimage.image.squareit()
        
        # resize the image and save it in gif format
        self.savegif(self.inimage, (500, 500))
       
    def calculate_bandpass(self, inradius, insmooth, outradius, outsmooth):
        ''' This method calculates the filter and saves the corresponding images
        the power spectrum (self.psimage) and the result of the filter
        (self.iftimage) in the temp folder
        '''
        
        #transfrom the image
        self.ftimage = ImgFFT(self.inimage.image)
        self.ftimage.ft()

        
        # create bandpass mask
        mask = Mask(self.inimage.image.data.shape)
        mask.bandpass(inradius, insmooth, outradius, outsmooth)
        self.ftimage.apply_mask(mask)

        # represent the masked ps
        self.ftimage.power_spectrum()
        self.psimage = ImagePath(self.name + "_ps", self.ftimage.ps, self.bufpath)
        self.savegif(self.psimage, (500, 500))        

        # calculate inverse transform
        self.ftimage.ift()
        self.iftimage = ImagePath(self.name + "ift", self.ftimage.imgifft, self.bufpath)
        self.savegif(self.iftimage, (500, 500))

    def savegif(self,imagepath, size):
        ''' Given a class imagepath and the size of the images, saves into the
        temp folder the associated image
        '''
        
        # calculate ft for resizing
        imft = ImgFFT(imagepath.image.data)
        imft.ft()
        im = imft.resize_image(size[0], size[1])
        
        # save resized image
        imsave(imagepath.gifname, im.data, format = "gif")
        
    def rm(self):
        if isdir(self.bufpath):
            rmtree(self.bufpath)
        
        
#==============================================================================
# Define GUI Object
#==============================================================================

class MyWidget(object):
    
    def __init__(self, root, mypathtoimage):
        # initialize the frame and the canvas
        self.frame = Frame(root)
        self.frame.pack()    
        
        self.mypathtoimage = mypathtoimage
        
        # initialize helper class
        self.helper = ImageManager(self.mypathtoimage)
        
        # define the menu
        menubar = Menu(self.frame)
        
        menufile = Menu(menubar, tearoff = 0)
        menufile.add_command(label = "Open file...", command = self.openfile)
        menubar.add_cascade(label = "File", menu = menufile)
        
        # add a label representing image data
        self.vstr_iminfo = StringVar()
        self.vstr_iminfo.set(" not init ")
        
        self.iminfolabel = Label(self.frame, textvariable = self.vstr_iminfo)
        self.iminfolabel.grid(row = 0, column = 0)
        
        # define the canvas display
        self.canvas = Canvas(self.frame, width=1500, height=500)
        self.canvas.grid(row = 1, column = 0)
        
        self.frame.image = {"inimage" : 0, "fft" : 0, "ift" : 0}
        self.canvasposition = {"inimage" : 0, "fft" : 500, "ift" : 1000}
        

        # create entries for bandpass
        Label(self.frame, text = "band pass values").grid(row = 2, column = 0)
        
        # create a new frame that contains 4 labels 4 entries
        entryframe = Frame(self.frame)
        entryframe.grid(row = 3, column = 0) 
        
        # define the entry names
        myvariablesnames = ["inradius", "insmooth", "outradius", "outsmooth"]
        std_values = [str(e) for e in [5, 2, 100, 10]] # default bp values
        
        self.entries = {}
        for i, element in enumerate(myvariablesnames):
            Label(entryframe,text = element).grid(column = i * 2, row = 0)
            self.entries[element] = Entry(entryframe)
            self.entries[element].insert(0,  std_values[i])
            self.entries[element].grid(column = i * 2 + 1, row = 0)
        
        # define a button calculate
        
        b = Button(entryframe, text = "Calculate", command = self.calculate)
        b.grid(row = 0, column = 10)
        
        root.config(menu = menubar)
        
        # build the save menu
        
        self.savedir = StringVar()
        self.savedir.set(self.helper.mainpath)
        
        # add save frame
        saveframe = Frame(self.frame)
        saveframe.grid(row = 4, column = 0)
  
        # define the entry names
        self.myvariablesnames = ["wkdir", "saveps", "saveift", "savecomp"]
        self.defvalues = [self.savedir.get(),
                     self.helper.name + "_ps",
                     self.helper.name + "_ift",
                     self.helper.name + "_comp"]
        self.myvar_savefilenames = {}
        
        self.savefilesentry = {}
        for i, element in enumerate(self.myvariablesnames):
            Label(saveframe,text = element).grid(column = 0, row = i)

            self.myvar_savefilenames[element] = StringVar()
            self.myvar_savefilenames[element].set(self.defvalues[i])
            
            self.savefilesentry[element] = Entry(saveframe, textvariable = self.myvar_savefilenames[element])
            self.savefilesentry[element].grid(column = 1, row = i)

        getdir = Button(saveframe, text = "get directory", command = self.getdirectory)
        getdir.grid(row = 0, column = 2)
        
        self.saveps = IntVar()
        self.saveift = IntVar()
        self.savecomp = IntVar()
        csaveps = Checkbutton(saveframe, text = "Save ps", variable = self.saveps,
                 onvalue = 1, offvalue = 0)
        csaveps.grid(column = 2, row = 1, sticky = "w")
        
        csaveps = Checkbutton(saveframe, text = "Save ift", variable = self.saveift,
                 onvalue = 1, offvalue = 0)
        csaveps.grid(column = 2, row = 2, sticky = "w")

        csaveps = Checkbutton(saveframe, text = "Save comp", variable = self.savecomp,
                 onvalue = 1, offvalue = 0)
        csaveps.grid(column = 2, row = 3, sticky = "w")
        
        #save button
        self.saveimgs_b = Button(saveframe, text = "save images",
                          state = 'disabled', command = self.saveimages)
        self.saveimgs_b.grid(column = 2, row = 4)
    
    def getdirectory(self):
        self.savedir.set(filedialog.askdirectory())
    
    def saveimages(self):
        wkdir = self.myvar_savefilenames["wkdir"].get()

        if self.saveps.get():
            print("saving ps image")
            filename = self.myvar_savefilenames["saveps"].get()
            print(wkdir)
            print(filename)
            self.helper.psimage.image.save(join(wkdir, filename + ".png"))

        if self.saveift.get():
            print("saving ift image")
            filename = self.myvar_savefilenames["saveift"].get()
            self.helper.iftimage.image.save(join(wkdir, filename + ".png"))    
            
        if self.savecomp.get():
            # not yet ready, adjust the images istograms to the 3sigma value
            print("saving composite image")
            filename = self.myvar_savefilenames["savecomp"].get()
            # put all 3 images together    
            newimage = deepcopy(self.helper.inimage.image)
            newimage.normalize()
            newimage.limit(1)
            
            psimage = self.helper.psimage.image
            psimage.normalize()
            psimage.limit(1)
            newimage.create_composite_right(psimage)
            
            iftimage = self.helper.iftimage.image
            iftimage.normalize()
            iftimage.limit(1)
            newimage.create_composite_right(iftimage)
            
            newimage.save(join(wkdir, filename + ".png"))
        
    def openfile(self):
        # clean the folder
        self.helper.rm()
        
        # ask for filename
        self.mypathtoimage = filedialog.askopenfilename()

        # initializate the helper class
        self.helper = ImageManager(self.mypathtoimage)
        self.helper.init_inimage()
        
        # update label
        self.vstr_iminfo.set(self.buildinfostr())
        
        # update save file
        self.savedir.set(self.helper.mainpath)

        # update the default values
        self.defvalues = [self.savedir.get(),
                          self.helper.name + "_ps",
                          self.helper.name + "_ift",
                          self.helper.name + "_comp"]
        
        # update file names
        for i, element in  enumerate(self.myvariablesnames):
            self.myvar_savefilenames[element].set(self.defvalues[i])
        
        # show the first image
        self.show_image(self.helper.inimage, "inimage")
        
        
    def calculate(self):
        # get the bandpass valeus
        inradius = self.entries["inradius"].get()
        insmooth = self.entries["insmooth"].get()
        outradius = self.entries["outradius"].get()
        outsmooth = self.entries["outsmooth"].get()

        
        self.helper.calculate_bandpass(int(inradius), int(insmooth), int(outradius), int(outsmooth))
        
        self.show_image(self.helper.psimage, "fft")
        
        self.show_image(self.helper.iftimage, "ift")
        
        self.saveimgs_b['state'] = 'normal'

    def show_image(self, image, name):
        inimage = PhotoImage(file = image.gifname)
        self.frame.image[name] = inimage
        self.canvas.create_image(self.canvasposition[name],0 , image = inimage, anchor = "nw")
    
    def buildinfostr(self):
        name = self.helper.inimage.name
        inspect = self.helper.inimage.image.inspect()
        return name + " | " + inspect
    
#==============================================================================
# Test environment     
#==============================================================================

if __name__ == "__main__":
    
    piccorrpath = "C:/Users/Mauro/Desktop/Vita Online/Programming/Picture cross corr/"
    
    img_path = "C:/Users/Mauro/Desktop/Vita Online/Programming/Picture cross corr/silentcam/dataset24/avg/correlation_images/corr_1497777846958.png"
    img_path = "C:/Users/Mauro/Desktop/Vita Online/Programming/Picture cross corr/Lenna.png"
    img_path = "C:/Users/Mauro/Desktop/Vita Online/Programming/Picture cross corr/silentcam/dataset24/avg/processed_images/proc_1497777845048.png"
    
    img_path = join(piccorrpath, "silentcam/dataset24/avg/results/avg.png")

    # initializate Tk root
    root = Tk()    
    m = MyWidget(root, img_path)
    
    # start the loop
    root.mainloop()
    
    # clean up    
    m.helper.rm()