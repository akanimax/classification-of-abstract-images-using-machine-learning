#!/usr/bin/python

from __future__ import print_function
import os
import sys
from PIL import Image

# static file paths defined here
media_path = "../../media/" # media path for the user uploaded images

def convert(image_file_path, dest_path):
	try:	
		img = Image.open(image_file_path) # throws IOError    
		img = img.resize((100, 100), Image.ANTIALIAS)
		img.save(dest_path + "/resized_" + image_file_path.split("/")[-1])

	except IOError: # if IOError is thrown, then the image is faulty
		print("image %s is faulty" %(image_file_path))

if(len(sys.argv) != 2):
	print("Filename not provided")
	sys.exit()

# get the filename
filename = sys.argv[1]
imgFile = os.path.join(media_path, filename)

# convert the file to 100x100 file.
convert(imgFile, os.path.join(media_path, "resized/"))

print("file resized successfully and stored")
