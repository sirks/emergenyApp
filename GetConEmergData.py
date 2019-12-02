# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 22:49:22 2019

@author: Jarvis
"""

import folium as fm
import numpy as np
import requests
from bs4 import BeautifulSoup
import json


#Get the  active emergency code from copernicus 
Acticeurl="https://emergency.copernicus.eu/mapping/list-of-activations-rapid"
resp = requests.get(Acticeurl)
soup=BeautifulSoup(resp.content, features='xml')
#search for activations
items =soup.findAll('tr')
Activelist=[]
for item in items:
    if 'background-color:#75b127' in str(item):
        found=str(item).find("EMS")
        active=str(item)[found:found+7]
        Activelist.append(active)
print(Activelist)

#Get the newest open activations
url='https://emergency.copernicus.eu/mapping/activations-rapid/feed'
resp = requests.get(url)
soup=BeautifulSoup(resp.content, features='xml')
#search for activations
items =soup.findAll('item')
jsondata={}
for number,item in  enumerate(items):
   # print(number)
    first = item.title.text
    #Select only string values with activation Code
    activation = first[1:8] # code
    if activation in Activelist:
        Info=first[10:len(first)]
        url='https://emergency.copernicus.eu/mapping/list-of-components/{}/aemfeed'.format(activation)
        resp = requests.get(url)
        soup=BeautifulSoup(resp.content, features='xml')
        #Scrape Polygons
        polygons =soup.findAll('georss:polygon')
        #m=fm.Map([46.90814465,14.3134518],zoom_start=10,tiles='OpenStreetMap')
        poldata=[]
        for pol in polygons:
            newpoly=[]
          #  print(str(pol)[16:len(pol)-18])
            polraw=str(pol)[16:len(pol)-18]
            polsplit=polraw.split(" ")
            a=0
            #print(len(polsplit)/2)
            for i in range(0,int(len(polsplit)/2)):
                newpoly.append(polsplit[a:a+2])
                a=a+2
            poldata.append(newpoly)
        
      #  print(activation)
        jsondata[activation]={
                "code":activation,
                "info":Info,
                "poldata":poldata
                }

#print(jsondata)
  #  for ponum, coor in enumerate(poldata):
    # print(coor)
  #       jsondata["Pol-"+str(ponum+1)]=coor
#print(jsondata)
with open("Emergency.txt","w") as outfile:
    json.dump(jsondata,outfile)
