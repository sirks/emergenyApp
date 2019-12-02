# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:50:53 2019

@author: Jarvis
"""

import json
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import mapping, shape
import sys
import GetConEmergData #import getEmergecyData will run it. 

#user location and radius 

deg_dis=10**3/111319.49079327357
usercir=Point(47.0911,13.2543).buffer(radius*deg_dis)

def userinpol(userlatlon,radius,jsondata):
    #look thriugh emergency code]
      #  print(jsondata)
        listlist=jsondata["poldata"]
        #loop through coodinated and get them as cloud then make them a Polygon
        for pol in listlist[0:len(listlist)]:
            plotpol=[]
            for cor in pol:
               cor=[float(i) for i in cor]
               plotpol.append(cor)
                
            pol=Polygon(plotpol)
            #check the use is in the palyon
          
            #print(pol.intersects(usercir))
            if pol.intersects(usercir)==True:
                return "yes"
        return "no"
            
def userdanger(latlon,radius):
    #get emergency data 
    with open("EMERGENCY.txt") as json_file:
            data = json.load(json_file)
            #loop through data find is user is in poldata 
            
    useremejson={} #dictionay for the emergency the use is close by 
    for code,item in data.items():
        try:
            emer="no"
            emer=userinpol(latlon,radius,item)
            if emer=="yes":
               useremejson[code]=item
            print("User in Emergeny area:"+code)
        except Exception as e:
                 print("Error in GPS distance, check columns names")
                 print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                 print(type(e))
                 print(e.args)
                 pass
    if len(useremejson.keys())==0:
        useremejson["User safe"]="No Emergency for the user"
        
    return useremejson
#test run
#latlon=[46.9705,13.1598]
#radius=1 #km           
#test=userdanger(latlon,radius) 
