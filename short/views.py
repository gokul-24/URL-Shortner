from django.shortcuts import render,redirect
from django.http import HttpResponse
import string
import random
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.contrib import messages

def generate_url(): # Generates a random,unique string of length 6 
    while(True):
        url= ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
        obj=URL.objects.filter(short_url=url)
        if(len(obj)>1):
            continue
        else:
            break
    return url

 
def save_Url(request,x):    # Saves the url in the database
    if x==0:
        longUrl=request.POST['long']
        obj=URL.objects.filter(long_url=longUrl)
        print(len(obj))
        if longUrl=="" or len(obj)>0:
            return ""
        shortURL=generate_url()
        
    else:
        longUrl=request.POST['api1']
        shortURL=short_api_bitly(longUrl)

        if shortURL is None:
            return ""

    obj=URL(long_url=longUrl,short_url=shortURL,flag=x)
    obj.save()
    return shortURL
        


def returnAllURL(request): #returns all the urls 
    updateClicks(0)
    res=requests.request("GET","http://127.0.0.1:8000/allurls/")
    print(type(res))
    return res


def short_api_bitly(longUrl): # Bit.ly API to shorten the link
    headers = {
                'Authorization': f"2ffe21bd5fd3bba5c2b21c720d17ac901d519cf1",
                'Content-Type': 'application/json',
            }

    data = { "long_url": longUrl, "domain": "bit.ly"}
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, json=data).json()
    return response.get('link')


def home(request):
    
    if request.method=="GET":
        res=returnAllURL(request)
        return render(request,"index.html",{'res':res.json()})

    elif request.method=="POST":
        
        if 'action' in request.POST:    # generates unique short url

            shortURL=save_Url(request,0)
 
        elif 'api' in request.POST:     # uses bit.ly API
            
            shortURL=save_Url(request,1)

        if shortURL=="":
            messages.info(request,"Long Url invalid or already shortened")
        
            return redirect('/')
        if(len(shortURL)==5):
            shortURL='127.0.0.1:8000/'+shortURL
        res=returnAllURL(request)
        return render(request,"index.html",{'shortURL':shortURL,'res':res.json()})


def updateClicks(obj):     # updates the clicks in the database 
    if obj==0:             # when 0 is passed to obj it updates the clicks on bit.ly links
        bit=URL.objects.filter(short_url__icontains="bit.ly")
        c=0
        for i in bit:    
            update=getClicks(i.short_url[8:])
            URL.objects.filter(short_url=i.short_url).update(clicks=update)

    else:                  # updates clicks of self generated links
        updatedClicks=obj[0].clicks+1
        obj.update(clicks=updatedClicks)
    
        
def redirectFunc(request,short):            #redirects the shorturl to their respective long url
    url1=URL.objects.filter(short_url=short)
    if len(url1)>0:
        updateClicks(url1)
        return redirect(url1[0].long_url)
    else:
        messages.info(request,"URL not found try again with differnt link")
        
        return redirect('/')
        

# API VIEW of URL DATABASE
# can be accessed at localhost:8000/allurls/ 
class URLAPI(APIView):
    def get(self,request):
        obj=reversed(URL.objects.all())
        serialize=URLSerializer(obj,many=True)
        return Response(serialize.data)
    
    def post(self,request):
        serializer1 = URLSerializer(data=request.data)
        
        if serializer1.is_valid():
            serializer1.save()
            return Response({'msg':'created'})
        return Response(serializer1.errors)




#updates bit.ly clicks
def getClicks(biturl):
    clicks=0
    headers = {
        'Authorization': f"2ffe21bd5fd3bba5c2b21c720d17ac901d519cf1",
    }
    
    url='https://api-ssl.bitly.com/v4/bitlinks/'+biturl+'/clicks'
    
    response = requests.get(url, headers=headers).json()
    for i in response['link_clicks']:
        clicks+=i['clicks']
    
    return clicks




def delete(request):
    obj=URL.objects.all()
    obj.delete()

    return HttpResponse("deleted")    

    