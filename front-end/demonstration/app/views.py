#from __future__ import print_function
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import subprocess as sp
import requests
import json
from scipy.spatial import distance
from multiprocessing import Process
import os

import os
import sys
from collections import namedtuple
from math import sqrt
import random
import operator
from PIL import Image, ImageDraw
from collections import defaultdict
import matplotlib.colors as colors


from scripts.Features.Dominant import *
from scripts.Features.GetFeatures import *
from scripts.DNN.Dnn_classify import *
from scripts.CNN.cnn_predictor import *

































# Create your views here.

def index(request):
    return HttpResponse('Hello World')

def test(request):
    return HttpResponse("test successfull")





def hashtagger(request):
    #lets assume the output from our backend is in the form of a json list
    jsonList=[]
    jsonList.append({"Artist": "Akanimax", "Style": "something", "Genre": "somethingelse", "ColouremotionAnalysis": "Angry", "Brushstroke": "Soft" })
    parsedData = []
    userData = {}
    for data in jsonList:
        userData['Artist'] = data['Artist']
        userData['Style'] = data['Style']
        userData['Genre'] = data['Genre']
        userData['ColouremotionAnalysis'] = data['ColouremotionAnalysis']
        userData['Brushstroke'] = data['Brushstroke']
        parsedData.append(userData)
    return render(request, 'app-templates/hashtagger.html', {'data': parsedData})

@ensure_csrf_cookie
def results(request):

    req1=request
    if request.method == "POST":
        file_key = None
        for file_key in sorted(request.FILES):
            pass
        wrapped_file = ImageFile(request.FILES[file_key])
        filename = wrapped_file.name
        fs = FileSystemStorage()
    fs.delete("source")
    filename = fs.save("source",request.FILES[file_key])
    uploaded_file_url = fs.url(filename)
    #print (uploaded_file_url+"******")
    print(uploaded_file_url.split("/")[-1])
    Results=controller(uploaded_file_url.split("/")[-1])
    

    keys=['EdgeCount','Pentagons','Triangles','Squares','Circles','HalfCircles','BlobCount','ColourCount']
    values=Results[2]

    feature_dict=dict(zip(keys,values))

    parsedData = []
    parsedData.append(Results[0])
    parsedData.append(feature_dict)
    parsedData.append(Results[3])    
    parsedData.append(Results[4])

    #parsedData.append(color_emotion)
    print (parsedData)
    return render(req1, 'app-templates/results.html', {'data': parsedData})



def controller(image_path):

    result_list=[]

    obj=Dominant_Color(image_path)
    obj.main()
    

    obj2=GetFeatures(image_path)
    obj2.returnFeatures()
    print ("features are...............")
    print (obj2.features) 

    cnn_target = get_predictions(image_path)	

    obj3 = DnnClassifier()
    obj3.returnProbabilities(obj2.features)
   
    dnn_target = obj3.label_probability	
    print(dnn_target)
    
    print(cnn_target)
    	
    def average(dict1,dict2):
    	dict3={}
    	for key in dict2.keys():
        	dict3[key]=(0.7*dict1[key]+0.3*dict2[key])
    	return dict3

    dict_cnn_target = dict(cnn_target)        

    dict_cnn_target['ActionPainting']=dict_cnn_target['Action-Painting']
    dict_cnn_target['Expressionism']=dict_cnn_target['art--Expressionism']
    del dict_cnn_target['Action-Painting']
    del dict_cnn_target['art--Expressionism']

    avg_result = average(dict_cnn_target, dnn_target)

    avg_result = sorted([(k, avg_result[k]) for k in avg_result.keys()], key=lambda x: x[1], reverse=True)
    dnn_target = sorted([(k, dnn_target[k]) for k in dnn_target.keys()], key=lambda x: x[1], reverse=True)	




    result_list.append(cnn_target[:3])
    result_list.append(obj.color_emotion)
    result_list.append(obj2.features)
    result_list.append(dnn_target[:3])	
    result_list.append(avg_result[:3])

    del obj3
    del obj2	

    return result_list

	




