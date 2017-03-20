
# coding: utf-8
#--- 2.12477397919 seconds ---

# # Script to Generate the Feature CSV FILE

# In[1]:
from multiprocessing import Process
from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage.feature import canny
from skimage import data
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import os
import csv 
import time
from scipy.spatial import distance
try:
    import Image
except ImportError:
    from PIL import Image


# In[2]:

class GetFeatures:
    filepath=""
    features=[]
    blackpath="media/black.png"
    TotalPent = 0
    TotalCircle = 0
    TotalHalfCircle = 0
    TotalSquare = 0
    TotalTri = 0
    color_dict = [(0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(127,127,127),(255,165,0),(255,255,0),(128,0,128),(165,42,42),(255,192,203)]
    edge_count=0
    shape_count=[None] * 5
    blob_count=0
    color_count=0


    def __init__(self,path):
       
		# static file paths defined here
		media_path = "/home/ccenter/new/17-02-2017_clone/BE/front-end/demonstration/media/" 
		# media path for the user uploaded images
		self.filepath = os.path.join(media_path, path)
		print (self.filepath)
		del self.features[:]
		




    def detectEdges(self,filename):
        image=io.imread(filename)
        edges = canny(image, 2, 1, 25)
        lines = probabilistic_hough_line(edges, threshold=10, line_length=10,
                                         line_gap=3)
        count=0
        for line in lines:
            p0, p1 = line
            count+=1
        return count
    
    def getBlobs(self,filepath):
        im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 10
        detector = cv2.SimpleBlobDetector(params)
        keypoints = detector.detect(im)
        self.blob_count= len(keypoints)
        
    
    def toBlack(self,image_file):
        im_gray = cv2.imread(image_file, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        str_path=self.blackpath
        cv2.imwrite(str_path, im_bw)
        cnt=self.detectEdges(str_path)
        self.edge_count= cnt
 
    def shapecount(self,string_path):
        img = cv2.imread(string_path)
        gray = cv2.imread(string_path,0)

        ret,thresh = cv2.threshold(gray,127,255,1)

        contours,h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        count_pent = 0
        count_tri = 0 
        count_sq  = 0
        count_halfcircle = 0  
        count_circle = 0 

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            if len(approx)==5:
                count_pent+=1
            elif len(approx)==3:
                count_tri+=1
            elif len(approx)==4:
                count_sq+=1
            elif len(approx) == 9:
                count_halfcircle+=1
            elif len(approx) > 9:
                count_circle+=1
    
        self.shape_count[0]=count_pent
	self.shape_count[1]=count_tri
	self.shape_count[2]=count_sq
	self.shape_count[3]=count_halfcircle
	self.shape_count[4]=count_circle

    def getColorCount(self,rgb_colors):
        flags = [0,0,0,0,0,0,0,0,0,0,0]
        min_dist = 999
        flag_pos = 11
        len_dict = len(self.color_dict)
        len_rgb = len(rgb_colors)
        final_count = 0

        for j in range(len_rgb):
            for i in range(len_dict):
                dst = distance.euclidean(self.color_dict[i],rgb_colors[j])
                if dst < min_dist:
                    min_dist = dst
                    flag_pos = i
            if flag_pos < 11:
                flags[flag_pos] = 1
        for i in range(len(flags)-1):
            if flags[i] == 1:
                final_count+=1
        return final_count
    
    def getColors(self,filepath):
        resize=100
        image = Image.open(filepath)
        image = image.resize((resize, resize))
        result = image.convert('RGB', palette=Image.ADAPTIVE, colors=24)
        result.putalpha(0)
        colors = result.getcolors(resize*resize)
        l=[]
        for color in colors:
            l.append(color[:][1])
        final_res=[]
        for i in l:
            final_res.append(list(i))

        for i in final_res:
            i.pop(3)
        rgb_colors = []
        for i in final_res:
            rgb_colors.append(tuple(i))
        col_count=self.getColorCount(rgb_colors)   
        self.color_count= col_count
    
    
    def returnFeatures(self):
	start_time = time.time()
        p1 = Process(target=self.toBlack(self.filepath))
	p1.start()  
	p2 = Process(target=self.getBlobs(self.filepath))
	p2.start() 
	p3 = Process(target=self.shapecount(self.filepath))
	p3.start()
	p4 = Process(target=self.getColors(self.filepath))
	p4.start()

	p1.join()
	p2.join()
	p3.join()
	p4.join()
        self.features=[self.edge_count,self.shape_count[0],self.shape_count[1],self.shape_count[2],self.shape_count[3],self.shape_count[4],self.blob_count,self.color_count]
	print("--- %s seconds ---" % (time.time() - start_time))


