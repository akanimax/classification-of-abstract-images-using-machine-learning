import numpy as np
import cv2
import os

class ShapesCount:
	TotalPent = 0
	TotalCircle = 0
	TotalHalfCircle = 0
	TotalSquare = 0
	TotalTri = 0
	
	def shapecount(self,string_path):
		#print string_path 
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
		    
		
		self.TotalPent += count_pent
		self.TotalTri += count_tri
		self.TotalSquare += count_sq
		self.TotalHalfCircle += count_halfcircle
		self.TotalCircle += count_circle

	def AvgCount(self,filecount):
		'''
		print "Pentagons:", self.TotalPent
		print "Triangles:", self.TotalTri
		print "Squares:", self.TotalSquare
		print "Circle:", self.TotalCircle
		print "HalfCircles:", self.TotalHalfCircle
		'''
		
		print "Pentagons:", self.TotalPent/filecount
		print "Triangles:", self.TotalTri/filecount
		print "Squares:", self.TotalSquare/filecount
		print "Circle:", self.TotalCircle/filecount
		print "HalfCircles:", self.TotalHalfCircle/filecount

	def readFile(self):
		print "Hello" 
		string_path = "/home/pict/Pindown/PinDown__Concretism/"
		filecount = 0

		for filename in os.listdir("/home/pict/Pindown/PinDown__Concretism/"):
			string_path = string_path + filename
			self.shapecount(string_path)
			string_path = "/home/pict/Pindown/PinDown__Concretism/"
			filecount+=1
		print "Total Files:", filecount
		self.AvgCount(filecount)
			

	
b = ShapesCount()
b.readFile()
	    
