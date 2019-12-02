
import requests
from bs4 import BeautifulSoup
import json

def GetActivePol(number):
    """
    
    """
    
    
    #Get the newest open activations
    url='https://emergency.copernicus.eu/mapping/activations-rapid/feed'
    resp = requests.get(url)
    soup=BeautifulSoup(resp.content, features='xml')
    
    #search for activations
    items =soup.findAll('item')
    first = items[number].title.text
    #Select only string values with activation Code
    activation = first[1:8] # code
    Info=first[10:len(first)]
    url='https://emergency.copernicus.eu/mapping/list-of-components/{}/aemfeed'.format(activation)
    resp = requests.get(url)
    soup=BeautifulSoup(resp.content, features='xml')
    #Scrape Polygons
    polygons =soup.findAll('georss:polygon')
    poldata=[]
    for pol in polygons:
      #  print(str(pol)[16:len(pol)-18])
        polraw=str(pol)[16:len(pol)-18]
        polsplit=polraw.split(" ")
        a=0
        #print(len(polsplit)/2)
        for i in range(0,int(len(polsplit)/2)):
            poldata.append(polsplit[a:a+2])
            a=a+2
    
        
        
    print(poldata)
  
    jsondata={}
    jsondata["active"]=[]
    jsondata["active"].append({
            "code":activation,
            "info":Info,
            "polygon":poldata
    
            })
    with open("data.txt","w") as outfile:
        json.dump(jsondata,outfile)
    
GetActivePol(0)
    
