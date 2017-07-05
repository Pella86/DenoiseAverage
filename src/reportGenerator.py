# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:48:41 2017

@author:Miriam
"""
import AvgFolder_class

class reportGenerator:

    def __init__(self, title, path):

        self.title = title
        self.path = path

    def generate():

        self.out_file = open(self.path + "/test.html","w")

        #create html page
        self.out_file.write("<html>\n<body>\n")
        #for futher use of styling
        self.out_file.write("<div class=\"report\">\n")

        #body of report
        #self.out_file.write("<p>DATASET #" + self.index +"</p>\n")
        self.out_file.write("<p>Dataset title</p>\n")
        self.out_file.write("<p>" + title + "</p>\n")

        #initial images
        self.out_file.write("<div class =\"dataset-img \">\n")
        self.out_file.write("<p>Dataset's photos</p>\n")

        self.imgs = AvgFolder_class.AvgFolderMem(self.path)

        for self.img_path in self.imgs.init_imgs.paths:
            self.out_file.write("<img src=\"" + self.img_path + "\">")
            pass

        self.out_file.write("</div>\n")

        #aligned images
        self.out_file.write("<div class =\"aligned-img \">\n")
        self.out_file.write("<p>Aligned Images</p>\n")

        for i, aligned_image in enumerate(self.imgs.algimgs):
            self.path_preview =  self.path + "/avg/aligned_images/algimage_" + str(i) + ".png"
            aligned_image.save(self.path_preview)
            self.out_file.write("<img src=\"" + self.path_preview + "\">")
            pass

        #correlation images
        self.out_file.write("<div class =\"correlation-img \">\n")
        self.out_file.write("<p>Correlation Images</p>\n")

        for i, correlation_image in enumerate(self.imgs.corrs):
            self.path_preview =  self.path + "/avg/correlation_images/correlation_" + str(i) + ".png"
            correlation_image.save(self.path_preview)
            self.out_file.write("<img src=\"" + self.path_preview + "\">")
            pass

        #processed images
        self.out_file.write("<div class =\"processed-img \">\n")
        self.out_file.write("<p>Processed Images</p>\n")

        for i, processed_image in enumerate(self.imgs.imgs):
            self.path_preview =  self.path + "/avg/processed_images/proc_imgs_" + str(i) + ".png"
            processed_image.save(self.path_preview)
            self.out_file.write("<img src=\"" + self.path_preview + "\">")
            pass

        self.out_file.write("</div>\n")
        self.out_file.write("</div>\n")
        self.out_file.write("</div>\n")

        #Template
        self.out_file.write("<p>Template used</p>\n")
        self.out_file.write("<img src=\"" + self.get_template_path() + "\">")
        #result
        self.out_file.write("<p>Result</p>\n")
        self.out_file.write("<img src=\"" + self.get_result_path() + "\">")

        #closing file
        self.out_file.write("</div>\n")
        self.out_file.write("</body>\n</html>\n")

        self.out_file.close()


    def get_template_path(self):

        self.template_path = self.path + "/avg/template.png"

        return self.template_path

    def get_result_path(self):

        self.result_path = self.path + "/avg/results/avg.png"

        return self.result_path


reportGenerator = reportGenerator("testdataset", "")
