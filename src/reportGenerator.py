# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:48:41 2017
@author:Miriam

"""
import AvgFolder_class
import shutil

from LogTimes import Logger
from pathlib import Path

class reportGenerator:

    def __init__(self, title, path):

        self.title = title
        self.path = path
        self.avg = AvgFolder_class.AvgFolderMem(self.path)

        self.mylog = Logger("Report Generator", self.avg.subfolders["results"] + "reportGeneratorlog.txt")

        # create a dictionary for the table
        # name of folder : "PathImageArray"
        self.tabledict = {"aligned_images": self.avg.algimgs, "correlation_images" : self.avg.corrs, "processed_images" : self.avg.imgs, "init_images" : self.avg.init_imgs}

    def create_image_table(self, tablename):
        #aligned images
        self.out_file.write('<div>\n')
        self.out_file.write('<header>'  + tablename + "</header>\n")

        patharray = self.tabledict[tablename]

        for i in range(patharray.n):
            path_preview = patharray.get_path_to_img(i)
            print(path_preview)
            p = Path(path_preview)
            self.out_file.write("<img src=" + '"' +  str(p.absolute()) + '" style="width:128px;"' + "/" + ">")

        self.out_file.write("\n</div>\n")

    def generate(self):

        self.mylog.log("Report generation started", True)

        shutil.copy2("./w3.css", self.path)

        self.out_file = open(self.path + "test.html","w")

        #create html page
        self.out_file.write("<html>\n<head>\n")
        self.out_file.write('<link rel="stylesheet" type="text/css" href="w3.css">\n')

        self.out_file.write("</head>\n<body>\n")

        self.out_file.write("<div>\n")

        #body of report
        #self.out_file.write("<p>DATASET #" + self.index +"</p>\n")
        self.out_file.write('<p id="title">' + self.title + "</p>\n")

        #initial images
        self.out_file.write("<div>\n")
        self.out_file.write('<p id="subtitle">Dataset\'s photos</p>\n')

        # create the image tables
        self.mylog.log("Opening initial images")
        self.create_image_table("init_images")
        self.create_image_table("aligned_images")
        self.create_image_table("correlation_images")
        self.create_image_table("processed_images")

        #Template
        self.out_file.write("<p>Template used</p>\n")
        self.out_file.write("<img src=\"" + str(Path(self.avg.get_template_path()).absolute()) + "\">")
        #result
        self.out_file.write("<p>Result</p>\n")
        self.out_file.write("<img src=\"" + str(Path(self.avg.get_avg_path()).absolute()) + "\">")

        self.t_log = open(self.path + "tlog/mytransformations.log","r")

        self.out_file.write('<p id="subtitle">Transformation Log</p>')
        self.out_file.write('<p>' + self.t_log.read() + '</p>')

        #closing file
        self.out_file.write("</div>\n")
        self.out_file.write("</body>\n</html>\n")

        self.out_file.close()

        self.mylog.log("Report generation done.", True)



if __name__ == "__main__":
    folders = ["testdataset"]

    for fldr in folders:
        folder = "" + fldr + "/"
        rGen = reportGenerator(fldr, folder)
        rGen.generate()
