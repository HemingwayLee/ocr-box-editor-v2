import json
import os
import re
import cv2
import pytesseract
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

    with open(os.path.splitext(path)[0] + ".box", "r") as boxfile:
        img = cv2.imread(os.path.splitext(path)[0] + ".png")
        height, width, _ = img.shape

        for line in boxfile:
            if "WordStr " in line:
                outer_idx = re.search(r' 0 #', line).start()
                coor = line[8:outer_idx]
                x, y, w, h = getCoor(coor, width, height)

                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 1)
        
        cv2.imwrite(os.path.splitext(path)[0] + ".jpg", img)

    return JsonResponse({"msg": "box file saved successfully"}, safe=False)

def listFiles(request):
    images = []
    for filename in os.listdir(settings.MEDIA_ROOT):
        if filename.endswith(".png"): 
            path = settings.MEDIA_ROOT + "/" + os.path.basename(filename)
            with open(os.path.splitext(path)[0] + ".box", encoding="utf-8") as boxfile:
                x = [l.rstrip("\n") for l in boxfile] 
            
            img = cv2.imread(os.path.splitext(path)[0] + ".tif")
            result = pytesseract.image_to_string(img, config="--psm 6", lang="eng")

            item = {
                "img": "http://127.0.0.1:8000/media/" + filename,
                "img2": "http://127.0.0.1:8000/media/" + os.path.splitext(os.path.basename(filename))[0] + ".jpg",
                "box": x[0].split("#",1)[1],
                "ori": result,
                "content": x[0]
            }

            images.append(item)

    return JsonResponse(dict(images=images), safe=False)

def getCoor(coor, width, height):
    each_coor = [int(i) for i in coor.split(' ')]
    y2 = height - each_coor[1]
    y1 = height - each_coor[3]

    each_coor[1] = y1
    each_coor[2] = each_coor[2] - each_coor[0]
    each_coor[3] = y2 - y1

    return each_coor[0], each_coor[1], each_coor[2], each_coor[3]

