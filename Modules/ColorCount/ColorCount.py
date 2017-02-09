'''
#pip install colorific
#pip install colorweave  --for dominant colors(not used)
#colorific -h --for the parameter explaination
min_prominence = The minimum proportion of pixels needed to keep a color
n_quantized = the larger the value more time but more accurate results
'''

'''Working of the code
	the extract color finds 24 colors and then they are passes to the avgColorCount to find minimum distance
	

'''

import os
from colorific import extract_colors, rgb_to_hex
from scipy.spatial import distance

class ColorCount:
	Total_count = 0
	color_dict = [(0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(127,127,127),(255,165,0),(255,255,0),(128,0,128),(165,42,42),(255,192,203)]
			
	
	def getAvgColorCount(self,rgb_colors):	
		flags = [0,0,0,0,0,0,0,0,0,0,0]		
		min_dist = 999
		flag_pos = 11
		len_dict = len(self.color_dict) - 1
		len_rgb = len(rgb_colors) - 1
		final_count = 0
		for i in range(len_dict):
			for j in range(len_rgb):
				dst = distance.euclidean(self.color_dict[i],rgb_colors[j])
				
				if dst < min_dist:
					min_dist = dst
					flag_pos = i
			if flag_pos < 11:
				flags[flag_pos] = 1
		print flags
		for i in range(len(flags)-1):
			if flags[i] == 1:
				final_count+=1
		
		print "Nearest colors count in color_dict",final_count		
			
	def getColors(self,filepath):		
		palette = extract_colors(filepath,max_colors=24,n_quantized = 200)
		rgb_colors = []
		for color in palette.colors:
			rgb_colors.append(color.value)
		self.getAvgColorCount(rgb_colors)
		
		
	def readFile(self):
		
		dirpath = "/home/pict/Project/PinDown/PinDown__Colour-Field-Painting/"
		
		for filename in os.listdir(dirpath):
			filepath = dirpath + filename
			print filename
			self.getColors(filepath)
	

b = ColorCount()
b.readFile()

