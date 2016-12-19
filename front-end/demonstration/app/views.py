from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import requests
import json

# Create your views here.

def index(request):
    return HttpResponse('Hello World')

def test(request):
    return HttpResponse("test successfull")



'''def profile(request):
    jsonList = []
    req = requests.get('https://api.github.com/users/akanimax')
    jsonList.append(json.loads(req.content))
    parsedData = []
    userData = {}
    for data in jsonList:
        userData['name'] = data['name']
        userData['blog'] = data['blog']
        userData['email'] = data['email']
        userData['public_gists'] = data['public_gists']
        userData['public_repos'] = data['public_repos']
        userData['avatar_url'] = data['avatar_url']
        userData['followers'] = data['followers']
        userData['following'] = data['following']
        parsedData.append(userData)
    return render(request, 'app-templates/profile.html', {'data': parsedData})'''


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
        filename = fs.save(filename, request.FILES[file_key])
        uploaded_file_url = fs.url(filename)
        print (uploaded_file_url)


        jsonList = controller()
        jsonList.append(
            {"Artist": "Akanimax", "Style": "something", "Genre": "somethingelse", "ColouremotionAnalysis": "Angry",
             "Brushstroke": "Soft"})
        parsedData = []
        userData = {}
        for data in jsonList:
            userData['Artist'] = data['Artist']
            userData['Style'] = data['Style']
            userData['Genre'] = data['Genre']
            userData['ColouremotionAnalysis'] = data['ColouremotionAnalysis']
            userData['Brushstroke'] = data['Brushstroke']
            parsedData.append(userData)
        return render(req1, 'app-templates/results.html', {'data': parsedData})

    return HttpResponse("error while storing image")


def controller():
    
    return json






