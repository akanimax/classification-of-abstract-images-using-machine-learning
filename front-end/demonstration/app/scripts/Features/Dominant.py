


import os
import sys
from collections import namedtuple
from math import sqrt
import random
import operator
from PIL import Image, ImageDraw
from collections import defaultdict
import matplotlib.colors as colors
from scipy.spatial import distance

try:
    import Image
except ImportError:
    from PIL import Image


class Dominant_Color:
	imgFile=""
	allpallettee="media/allpallettee.png"
	dominant="media/dominant.png"
	Point = namedtuple('Point', ('coords', 'n', 'ct'))
	Cluster = namedtuple('Cluster', ('points', 'center', 'n'))
	rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))
	result=[]
	color_emotion={}


	def GiveMeEmotion(self,rgb_value):
		dict = {
			'White': (255,255,255),
			'Black':(0,0,0),
			'Gray':(127,127,127),
			'Red':(255,0,0),
			'Orange':(255,128,0), 
		        'Yellow':(255,255,0),
		        'Green':(0,255,0),
			'Blue':	(0,0,255),
			'Purple':(128,0,128),
			'Brown':(165,42,42),
			'Pink':(255,192,203)
			}
		min_dist=999
		emotion={
			'White': ["purity","innocence","cleanliness","mourning (in some cultures/societies)","neutrality"],
			'Black':["evil","strength","power","mourning (in some cultures/societies)","intelligence","authority"],
			'Gray':["timeless","practical","neutrality"],
			'Red':["love","romance","intensity","life","blood","energy","excitement"],
			'Orange':["happy","energetic","enthusiasm","warmth","stimulation","change"],
			'Yellow':["happiness","laughter","warmth","optimism","frustration","attention-getting"],
			'Green':["purity","cool","growth","natural","tranquility","harmony","calmness"],
			'Blue':["serenity","cold","uncaring","calmness","focused"],
			'Purple':["royalty","wealth","sophistication","prosperity","respect","mystery"],
			'Brown':["reliability","stability","sadness","mourning (in some cultures/societies)","organic"],
			'Pink':["romance","love","calming","gentle","agitation"]
			}
		for i in dict:
			dst = distance.euclidean(rgb_value,dict[i])
			if dst<=min_dist:
				min_dist=dst
				color=i
		#print min_dist
		#print color
		#print emotion[color]
		self.color_emotion[color]=emotion[color]
		print (color)
		print ("Emotions")		
		print (emotion[color])
		
	def __init__(self, path):
		print ("***************"+path)
		# static file paths defined here
		media_path = "/home/botman/Programming/Machine_Learning/BE/front-end/demonstration/media/" # media path for the user uploaded images
		self.imgFile = os.path.join(media_path, path)
		print (self.imgFile)
		self.color_emotion.clear()
		'''self.allpallettee=self.imgFile+".allpallettee.png"
		print (self.allpallettee)
		self.dominant=self.imgFile+"_dominant.png"
		print (self.dominant)'''





	def get_points(self,img):
	    points = []
	    w, h = img.size
	    for count, color in img.getcolors(w * h):
		points.append(self.Point(color, 3, count))
	    return points


	def colorz(self,filename, n=3):
	    
	    img = Image.open(filename)
	    img.thumbnail((200, 200))
	    w, h = img.size

	    points = self.get_points(img)
	    clusters = self.kmeans(points, n, 1)
	    rgbs = [map(int, c.center.coords) for c in clusters]
	    return map(lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb)), rgbs)

	def euclidean(self,p1, p2):
	    return sqrt(sum([(p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)]))

	def calculate_center(self,points, n):
	    vals = [0.0 for i in range(n)]
	    plen = 0
	    for p in points:
		plen += p.ct
		for i in range(n):
		    vals[i] += (p.coords[i] * p.ct)
	    return self.Point([(v / plen) for v in vals], n, 1)

	def kmeans(self,points, k, min_diff):
	    clusters = [self.Cluster([p], p, p.n) for p in random.sample(points, k)]

	    while 1:
		plists = [[] for i in range(k)]

		for p in points:
		    smallest_distance = float('Inf')
		    for i in range(k):
		        distance = self.euclidean(p, clusters[i].center)
		        if distance < smallest_distance:
		            smallest_distance = distance
		            idx = i
		    plists[idx].append(p)

		diff = 0
		for i in range(k):
		    old = clusters[i]
		    center = self.calculate_center(plists[i], old.n)
		    new = self.Cluster(plists[i], center, old.n)
		    clusters[i] = new
		    diff = max(diff,self.euclidean(old.center, new.center))

		if diff < min_diff:
		    break

	    return clusters

	def get_colors(self,infile, outfile, numcolors=10, swatchsize=20, resize=150):
	    print ("infile is"+infile)
	    image = Image.open(infile)
	    image = image.resize((resize, resize))
	    self.result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
	    print (self.result)
	    self.result.putalpha(0)
	    colors = self.result.getcolors(resize*resize)
	    #print colors
	    
	    # Save colors to file

	    pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
	    draw = ImageDraw.Draw(pal)

	    posx = 0
	    for count, col in colors:
	
		draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
		posx = posx + swatchsize

	    del draw
	    pal.save(outfile, "PNG")
	    return len(colors)

	def dumpToSwatch(self,outfile,max_colors,numcolors=2, swatchsize=20):
	    pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
	    draw = ImageDraw.Draw(pal)

	    posx = 0
	    for count, col in max_colors:
	
		draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
		posx = posx + swatchsize

	    del draw
	    pal.save(outfile, "PNG")

	def dumpToSwatch(self,outfile,max_colors,numcolors=2, swatchsize=20):
	    pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
	    draw = ImageDraw.Draw(pal)

	    posx = 0
	    for col in max_colors:
	
		draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
		posx = posx + swatchsize

	    del draw
	    pal.save(outfile, "PNG")

	def hex_to_rgb(self,value):
	    """Return (red, green, blue) for the color given as #rrggbb."""
	    value = value.lstrip('#')
	    lv = len(value)
	    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


    
	def main(self):
	    array = []
	    result1=[]
	    sanity_check=self.get_colors(self.imgFile,self.allpallettee)
	    #print(sanity_check)
	    if(sanity_check>4):
		    for i in range (5):
			    array.append(self.colorz(self.imgFile,n=4))    
		    for i in range (5):
				for j in range (4):
					result1.append(array[i][j])	
		    #print result 
		    d = defaultdict(int)
		    for i in result1:
			d[i] += 1
		    #print d
		    result_final = max(d.iteritems(), key=lambda x: x[1])
		    sortedA = sorted(d.items(), key=operator.itemgetter(1),reverse=True)
		    
		    #print sortedA[:2]
		    sortedA=sortedA[:2]

		    max_colors=[]
		    desired_list=[]    			

		    for i in range(len(sortedA)):

			max_colors.append(self.hex_to_rgb(sortedA[i][0]))
		    for rgb_color in max_colors:
			#print (rgb_color)
			self.GiveMeEmotion(rgb_color)
		    value=0	

		    desired_list = [tuple(list(tup)+[value]) for tup in max_colors]
	     	    #print desired_list
		    self.dumpToSwatch(self.dominant,desired_list)
		    print("value being returned is")
		    print (self.color_emotion)

