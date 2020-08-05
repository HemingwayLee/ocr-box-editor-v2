import json
import os
from subprocess import call
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

def index(request):
    return render(request, 'index.html', {"address": "127.0.0.1"})

def listPage(request):
    return render(request, 'data.html', {"address": "127.0.0.1"})

@csrf_exempt
def processImage(request):
    
    if request.method == 'POST' and request.FILES['fileName']:
        myfile = request.FILES['fileName']
        path = settings.MEDIA_ROOT + "/" + myfile.name
        if os.path.exists(path):
            return JsonResponse({"msg": "file already exist"}, safe=False)

        fss = FileSystemStorage()
        fss.save(myfile.name, myfile)
        fss.save(os.path.splitext(path)[0] + ".png", myfile) # Save another png file for display
        
        # calling and waiting
        call(["scripts/generator.sh", path, "eng"])

        with open(os.path.splitext(path)[0] + ".box", encoding="utf-8") as boxfile:
            x = [l.rstrip("\n") for l in boxfile] 

        return JsonResponse({"msg": "file processed successfully", "data": x[0]}, safe=False)
    else:
        return JsonResponse({"msg": "file not exist"}, safe=False)

@csrf_exempt
def updateBoxfile(request):
    data = request.body.decode('utf-8') 
    jsonData = json.loads(data)

    print(jsonData["filename"])
    print(jsonData["content"])

    path = settings.MEDIA_ROOT + "/" + os.path.basename(jsonData["filename"])
    with open(os.path.splitext(path)[0] + ".box", encoding="utf-8", mode="w+") as boxfile:
        boxfile.write(jsonData["content"])

    return JsonResponse({"msg": "box file saved successfully"}, safe=False)

def listFiles(request):
    images = []
    for filename in os.listdir(settings.MEDIA_ROOT):
        if filename.endswith(".png"): 
            path = settings.MEDIA_ROOT + "/" + os.path.basename(filename)
            with open(os.path.splitext(path)[0] + ".box", encoding="utf-8") as boxfile:
                x = [l.rstrip("\n") for l in boxfile] 
            
            item = {
                "img": "http://127.0.0.1:8000/media/" + filename,
                "box": x[0].split("#",1)[1]
            }

            images.append(item)

    return JsonResponse(dict(images=images), safe=False)
